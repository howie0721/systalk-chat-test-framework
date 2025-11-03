"""
AI/LLM 指標收集器
收集和匯出 AI 模型相關的品質指標
"""
import logging
from typing import Dict, Any, Optional
from monitoring.observability import get_observability

logger = logging.getLogger(__name__)


class AIMetricsCollector:
    """AI 指標收集器，整合各種 AI 測試工具的指標"""

    def __init__(self):
        self.observability = get_observability()

    def record_response_quality(self, model_name: str, metrics: Dict[str, Any]) -> None:
        """
        記錄回應品質指標

        Args:
            model_name: 模型名稱
            metrics: 品質指標字典，包含 coherence, relevance, fluency, completeness 等
        """
        try:
            # 記錄各項品質分數
            for metric_name, value in metrics.items():
                if isinstance(value, (int, float)):
                    self.observability.record_ai_metric(
                        model_name=model_name,
                        metric_name=f"response_quality.{metric_name}",
                        value=float(value),
                        labels={"metric_type": "quality", "component": metric_name},
                    )

            # 如果有總分，記錄總分
            if "overall_score" in metrics:
                self.observability.record_ai_metric(
                    model_name=model_name,
                    metric_name="response_quality.overall",
                    value=float(metrics["overall_score"]),
                    labels={"metric_type": "quality", "component": "overall"},
                )

            logger.debug(f"Recorded quality metrics for {model_name}: {metrics}")
        except Exception as e:
            logger.error(f"Failed to record quality metrics: {e}")

    def record_hallucination_detection(self, model_name: str, detection_result: Dict[str, Any]) -> None:
        """
        記錄幻覺檢測結果

        Args:
            model_name: 模型名稱
            detection_result: 檢測結果，包含 is_hallucination, confidence, risk_level 等
        """
        try:
            # 記錄是否為幻覺（1表示是，0表示否）
            is_hallucination = 1.0 if detection_result.get("is_hallucination", False) else 0.0
            self.observability.record_ai_metric(
                model_name=model_name,
                metric_name="hallucination.detected",
                value=is_hallucination,
                labels={"metric_type": "hallucination", "component": "detection"},
            )

            # 記錄信心度
            if "confidence" in detection_result:
                self.observability.record_ai_metric(
                    model_name=model_name,
                    metric_name="hallucination.confidence",
                    value=float(detection_result["confidence"]),
                    labels={"metric_type": "hallucination", "component": "confidence"},
                )

            # 記錄風險等級（轉換為數值）
            risk_level_map = {"low": 1.0, "medium": 2.0, "high": 3.0, "critical": 4.0}
            risk_level = detection_result.get("risk_level", "low")
            if risk_level in risk_level_map:
                self.observability.record_ai_metric(
                    model_name=model_name,
                    metric_name="hallucination.risk_level",
                    value=risk_level_map[risk_level],
                    labels={"metric_type": "hallucination", "component": "risk", "level": risk_level},
                )

            logger.debug(f"Recorded hallucination metrics for {model_name}: {detection_result}")
        except Exception as e:
            logger.error(f"Failed to record hallucination metrics: {e}")

    def record_drift_detection(self, model_name: str, drift_result: Dict[str, Any]) -> None:
        """
        記錄模型漂移檢測結果

        Args:
            model_name: 模型名稱
            drift_result: 漂移檢測結果，包含 drift_detected, drift_score, severity 等
        """
        try:
            # 記錄是否檢測到漂移
            drift_detected = 1.0 if drift_result.get("drift_detected", False) else 0.0
            self.observability.record_ai_metric(
                model_name=model_name,
                metric_name="drift.detected",
                value=drift_detected,
                labels={"metric_type": "drift", "component": "detection"},
            )

            # 記錄漂移分數
            if "drift_score" in drift_result:
                self.observability.record_ai_metric(
                    model_name=model_name,
                    metric_name="drift.score",
                    value=float(drift_result["drift_score"]),
                    labels={"metric_type": "drift", "component": "score"},
                )

            # 記錄嚴重程度
            severity_map = {"low": 1.0, "medium": 2.0, "high": 3.0}
            severity = drift_result.get("severity", "low")
            if severity in severity_map:
                self.observability.record_ai_metric(
                    model_name=model_name,
                    metric_name="drift.severity",
                    value=severity_map[severity],
                    labels={"metric_type": "drift", "component": "severity", "level": severity},
                )

            # 記錄變化百分比
            if "change_percentage" in drift_result:
                self.observability.record_ai_metric(
                    model_name=model_name,
                    metric_name="drift.change_percentage",
                    value=float(drift_result["change_percentage"]),
                    labels={"metric_type": "drift", "component": "change"},
                )

            logger.debug(f"Recorded drift metrics for {model_name}: {drift_result}")
        except Exception as e:
            logger.error(f"Failed to record drift metrics: {e}")

    def record_bias_detection(self, model_name: str, bias_result: Dict[str, Any]) -> None:
        """
        記錄偏見檢測結果

        Args:
            model_name: 模型名稱
            bias_result: 偏見檢測結果，包含 bias_detected, bias_score, bias_types 等
        """
        try:
            # 記錄是否檢測到偏見
            bias_detected = 1.0 if bias_result.get("bias_detected", False) else 0.0
            self.observability.record_ai_metric(
                model_name=model_name,
                metric_name="bias.detected",
                value=bias_detected,
                labels={"metric_type": "bias", "component": "detection"},
            )

            # 記錄偏見分數
            if "bias_score" in bias_result:
                self.observability.record_ai_metric(
                    model_name=model_name,
                    metric_name="bias.score",
                    value=float(bias_result["bias_score"]),
                    labels={"metric_type": "bias", "component": "score"},
                )

            # 記錄公平性分數
            if "fairness_score" in bias_result:
                self.observability.record_ai_metric(
                    model_name=model_name,
                    metric_name="bias.fairness_score",
                    value=float(bias_result["fairness_score"]),
                    labels={"metric_type": "bias", "component": "fairness"},
                )

            # 記錄各種偏見類型
            bias_types = bias_result.get("bias_types", {})
            for bias_type, score in bias_types.items():
                if isinstance(score, (int, float)):
                    self.observability.record_ai_metric(
                        model_name=model_name,
                        metric_name=f"bias.type.{bias_type}",
                        value=float(score),
                        labels={"metric_type": "bias", "component": "type", "bias_type": bias_type},
                    )

            logger.debug(f"Recorded bias metrics for {model_name}: {bias_result}")
        except Exception as e:
            logger.error(f"Failed to record bias metrics: {e}")

    def record_performance_metrics(self, model_name: str, metrics: Dict[str, Any]) -> None:
        """
        記錄模型性能指標

        Args:
            model_name: 模型名稱
            metrics: 性能指標，包含 latency, token_count, cost 等
        """
        try:
            # 記錄延遲
            if "latency" in metrics:
                self.observability.record_ai_metric(
                    model_name=model_name,
                    metric_name="performance.latency",
                    value=float(metrics["latency"]),
                    labels={"metric_type": "performance", "component": "latency"},
                )

            # 記錄 token 數量
            if "token_count" in metrics:
                self.observability.record_ai_metric(
                    model_name=model_name,
                    metric_name="performance.token_count",
                    value=float(metrics["token_count"]),
                    labels={"metric_type": "performance", "component": "tokens"},
                )

            # 記錄成本
            if "cost" in metrics:
                self.observability.record_ai_metric(
                    model_name=model_name,
                    metric_name="performance.cost",
                    value=float(metrics["cost"]),
                    labels={"metric_type": "performance", "component": "cost"},
                )

            # 記錄吞吐量
            if "throughput" in metrics:
                self.observability.record_ai_metric(
                    model_name=model_name,
                    metric_name="performance.throughput",
                    value=float(metrics["throughput"]),
                    labels={"metric_type": "performance", "component": "throughput"},
                )

            logger.debug(f"Recorded performance metrics for {model_name}: {metrics}")
        except Exception as e:
            logger.error(f"Failed to record performance metrics: {e}")

    def create_monitoring_context(self, model_name: str, operation: str):
        """
        創建監控上下文管理器，用於追蹤 AI 操作

        Args:
            model_name: 模型名稱
            operation: 操作名稱

        Returns:
            Context manager 用於追蹤
        """
        return self.observability.create_span(
            f"ai_operation: {operation}", {"model.name": model_name, "operation": operation}
        )


# 全域實例
_ai_metrics_collector: Optional[AIMetricsCollector] = None


def get_ai_metrics_collector() -> AIMetricsCollector:
    """獲取全域 AI 指標收集器實例"""
    global _ai_metrics_collector
    if _ai_metrics_collector is None:
        _ai_metrics_collector = AIMetricsCollector()
    return _ai_metrics_collector
