"""
Pytest plugin for OpenTelemetry integration
自動收集測試執行的追蹤和指標
"""
import pytest
import time
from typing import Optional
from monitoring.observability import get_observability
import logging

logger = logging.getLogger(__name__)


class TestMetricsCollector:
    """測試指標收集器"""

    def __init__(self):
        self.observability = None
        self.test_start_times = {}
        self.session_start_time = None

    def pytest_configure(self, config):
        """Pytest 配置階段"""
        # 初始化 Observability
        try:
            enable_console = config.getoption("--trace-console", default=False)
            enable_otlp = config.getoption("--trace-otlp", default=False)
            enable_prometheus = config.getoption("--metrics-prometheus", default=False)

            self.observability = get_observability(
                service_name="systalk-test-framework",
                enable_console=enable_console,
                enable_otlp=enable_otlp,
                enable_prometheus=enable_prometheus,
            )
            logger.info("Test metrics collector initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize observability: {e}")

    def pytest_sessionstart(self, session):
        """測試會話開始"""
        self.session_start_time = time.time()
        if self.observability:
            with self.observability.create_span("test_session", {"session.id": str(id(session))}):
                logger.debug("Test session started")

    def pytest_runtest_logstart(self, nodeid, location):
        """測試開始執行"""
        self.test_start_times[nodeid] = time.time()

        if self.observability:
            # 創建測試追蹤 span
            span_name = f"test: {nodeid}"
            attributes = {
                "test.name": nodeid,
                "test.file": location[0],
                "test.line": location[1],
                "test.function": location[2],
            }
            # 注意：這裡我們只記錄開始，實際的 span 在 runtest_makereport 中完成
            logger.debug(f"Test started: {nodeid}")

    def pytest_runtest_makereport(self, item, call):
        """測試報告生成"""
        if call.when == "call":  # 只在實際測試執行階段記錄
            nodeid = item.nodeid
            start_time = self.test_start_times.get(nodeid)

            if start_time and self.observability:
                duration = time.time() - start_time
                status = "passed" if call.excinfo is None else "failed"

                # 記錄測試指標
                self.observability.record_test_metric(test_name=nodeid, status=status, duration=duration)

                # 創建追蹤 span
                with self.observability.create_span(
                    f"test: {nodeid}",
                    {
                        "test.name": nodeid,
                        "test.status": status,
                        "test.duration": duration,
                        "test.outcome": call.outcome if hasattr(call, "outcome") else "unknown",
                    },
                ) as span:
                    if call.excinfo:
                        span.set_attribute("test.error", str(call.excinfo.value))

                logger.debug(f"Test completed: {nodeid} - {status} - {duration:.3f}s")

    def pytest_sessionfinish(self, session, exitstatus):
        """測試會話結束"""
        if self.session_start_time and self.observability:
            session_duration = time.time() - self.session_start_time

            # 記錄會話指標
            total_tests = session.testscollected
            passed = session.testscollected - session.testsfailed
            failed = session.testsfailed

            # 創建會話 span
            with self.observability.create_span(
                "test_session_complete",
                {
                    "session.duration": session_duration,
                    "session.total_tests": total_tests,
                    "session.passed": passed,
                    "session.failed": failed,
                    "session.exit_status": exitstatus,
                },
            ):
                logger.info(
                    f"Test session finished: {total_tests} tests, "
                    f"{passed} passed, {failed} failed in {session_duration:.2f}s"
                )

    def pytest_unconfigure(self, config):
        """Pytest 清理階段"""
        if self.observability:
            self.observability.shutdown()
            logger.info("Test metrics collector shutdown")


def pytest_addoption(parser):
    """添加命令行選項"""
    group = parser.getgroup("monitoring", "Test monitoring and observability options")

    group.addoption(
        "--trace-console",
        action="store_true",
        default=False,
        help="Enable console tracing output",
    )

    group.addoption(
        "--trace-otlp",
        action="store_true",
        default=False,
        help="Enable OTLP tracing export (to Jaeger/Grafana Tempo)",
    )

    group.addoption(
        "--metrics-prometheus",
        action="store_true",
        default=False,
        help="Enable Prometheus metrics export",
    )


def pytest_configure(config):
    """註冊 plugin"""
    config.pluginmanager.register(TestMetricsCollector(), "test_metrics_collector")
