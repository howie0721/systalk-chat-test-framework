"""
OpenTelemetry 監控整合
提供測試執行的可觀測性（Observability）
"""
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from prometheus_client import start_http_server
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class TestObservability:
    """測試可觀測性管理器"""

    def __init__(
        self,
        service_name: str = "systalk-test-framework",
        environment: str = "dev",
        enable_console: bool = True,
        enable_otlp: bool = False,
        enable_prometheus: bool = False,
        prometheus_port: int = 9464,
    ):
        """
        初始化測試可觀測性

        Args:
            service_name: 服務名稱
            environment: 環境名稱（dev, staging, prod）
            enable_console: 是否啟用控制台輸出
            enable_otlp: 是否啟用 OTLP 導出（到 Grafana/Jaeger）
            enable_prometheus: 是否啟用 Prometheus metrics
            prometheus_port: Prometheus metrics 服務埠
        """
        self.service_name = service_name
        self.environment = environment

        # 設定 Resource（服務識別資訊）
        self.resource = Resource.create(
            {
                "service.name": service_name,
                "service.version": "1.0.0",
                "deployment.environment": environment,
            }
        )

        # 初始化 Tracer 和 Meter
        self.tracer_provider = None
        self.meter_provider = None
        self.tracer = None
        self.meter = None

        # 設定追蹤（Tracing）
        self._setup_tracing(enable_console, enable_otlp)

        # 設定指標（Metrics）
        self._setup_metrics(enable_console, enable_otlp, enable_prometheus, prometheus_port)

        # 自動檢測 HTTP requests
        RequestsInstrumentor().instrument()

        logger.info(f"Test Observability initialized for {service_name} in {environment}")

    def _setup_tracing(self, enable_console: bool, enable_otlp: bool):
        """設定分散式追蹤"""
        self.tracer_provider = TracerProvider(resource=self.resource)

        # Console Exporter（開發用）
        if enable_console:
            console_exporter = ConsoleSpanExporter()
            console_processor = BatchSpanProcessor(console_exporter)
            self.tracer_provider.add_span_processor(console_processor)
            logger.debug("Console span exporter enabled")

        # OTLP Exporter（生產用 - 發送到 Grafana Tempo/Jaeger）
        if enable_otlp:
            otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
            try:
                otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
                otlp_processor = BatchSpanProcessor(otlp_exporter)
                self.tracer_provider.add_span_processor(otlp_processor)
                logger.info(f"OTLP span exporter enabled: {otlp_endpoint}")
            except Exception as e:
                logger.warning(f"Failed to initialize OTLP exporter: {e}")

        # 設定為全局 tracer
        trace.set_tracer_provider(self.tracer_provider)
        self.tracer = trace.get_tracer(__name__)

    def _setup_metrics(self, enable_console: bool, enable_otlp: bool, enable_prometheus: bool, prometheus_port: int):
        """設定指標收集"""
        readers = []

        # Console Metric Reader（開發用）
        if enable_console:
            console_reader = PeriodicExportingMetricReader(ConsoleMetricExporter(), export_interval_millis=60000)
            readers.append(console_reader)
            logger.debug("Console metric reader enabled")

        # OTLP Metric Reader（生產用 - 發送到 Grafana）
        if enable_otlp:
            otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
            try:
                otlp_metric_exporter = OTLPMetricExporter(endpoint=otlp_endpoint, insecure=True)
                otlp_reader = PeriodicExportingMetricReader(otlp_metric_exporter, export_interval_millis=60000)
                readers.append(otlp_reader)
                logger.info(f"OTLP metric exporter enabled: {otlp_endpoint}")
            except Exception as e:
                logger.warning(f"Failed to initialize OTLP metric exporter: {e}")

        # Prometheus Metric Reader
        if enable_prometheus:
            try:
                prometheus_reader = PrometheusMetricReader()
                readers.append(prometheus_reader)
                # 啟動 Prometheus HTTP 服務器
                start_http_server(prometheus_port)
                logger.info(f"Prometheus metrics server started on port {prometheus_port}")
            except Exception as e:
                logger.warning(f"Failed to start Prometheus server: {e}")

        # 創建 MeterProvider
        self.meter_provider = MeterProvider(resource=self.resource, metric_readers=readers)
        metrics.set_meter_provider(self.meter_provider)
        self.meter = metrics.get_meter(__name__)

    def create_span(self, name: str, attributes: Optional[dict] = None):
        """
        創建一個追蹤 span

        Args:
            name: Span 名稱
            attributes: Span 屬性

        Returns:
            Span context manager
        """
        from contextlib import contextmanager

        @contextmanager
        def span_context():
            with self.tracer.start_as_current_span(name) as span:
                if attributes:
                    for key, value in attributes.items():
                        span.set_attribute(key, value)
                yield span

        return span_context()

    def record_test_metric(self, test_name: str, status: str, duration: float):
        """
        記錄測試指標

        Args:
            test_name: 測試名稱
            status: 測試狀態（passed, failed, skipped）
            duration: 測試執行時間（秒）
        """
        # 測試計數器
        test_counter = self.meter.create_counter(
            name="test_executions_total", description="Total number of test executions", unit="1"
        )
        test_counter.add(1, {"test.name": test_name, "test.status": status, "environment": self.environment})

        # 測試執行時間
        test_duration = self.meter.create_histogram(
            name="test_duration_seconds", description="Test execution duration", unit="s"
        )
        test_duration.record(duration, {"test.name": test_name, "test.status": status, "environment": self.environment})

    def record_ai_metric(self, model_name: str, metric_name: str, value: float, labels: Optional[dict] = None):
        """
        記錄 AI 模型指標

        Args:
            model_name: 模型名稱
            metric_name: 指標名稱
            value: 指標值
            labels: 額外標籤
        """
        attributes = {"model.name": model_name, "environment": self.environment}
        if labels:
            attributes.update(labels)

        # AI 指標 gauge
        ai_gauge = self.meter.create_gauge(name=f"ai_{metric_name}", description=f"AI model {metric_name}")
        ai_gauge.set(value, attributes)

    def shutdown(self):
        """關閉監控"""
        if self.tracer_provider:
            self.tracer_provider.shutdown()
        if self.meter_provider:
            self.meter_provider.shutdown()
        logger.info("Test Observability shutdown")


# 全局實例（單例模式）
_observability_instance: Optional[TestObservability] = None


def get_observability(
    service_name: str = "systalk-test-framework",
    environment: str = None,
    enable_console: bool = True,
    enable_otlp: bool = False,
    enable_prometheus: bool = False,
) -> TestObservability:
    """
    獲取或創建全局 Observability 實例

    Args:
        service_name: 服務名稱
        environment: 環境名稱
        enable_console: 是否啟用控制台輸出
        enable_otlp: 是否啟用 OTLP
        enable_prometheus: 是否啟用 Prometheus

    Returns:
        TestObservability 實例
    """
    global _observability_instance

    if _observability_instance is None:
        # 從環境變數讀取配置
        if environment is None:
            environment = os.getenv("ENVIRONMENT", "dev")

        enable_otlp = enable_otlp or os.getenv("ENABLE_OTLP", "false").lower() == "true"
        enable_prometheus = enable_prometheus or os.getenv("ENABLE_PROMETHEUS", "false").lower() == "true"

        _observability_instance = TestObservability(
            service_name=service_name,
            environment=environment,
            enable_console=enable_console,
            enable_otlp=enable_otlp,
            enable_prometheus=enable_prometheus,
        )

    return _observability_instance
