"""
DriftMonitor - 模型漂移監控器
監控模型輸出是否隨時間產生顯著變化
"""
from typing import Dict, List, Optional
from datetime import datetime
import statistics
import logging

logger = logging.getLogger(__name__)


class DriftMonitor:
    """模型漂移監控器 - 追蹤模型行為變化"""
    
    def __init__(self, baseline_threshold: float = 0.15):
        """
        初始化漂移監控器
        
        Args:
            baseline_threshold: 允許的基準偏差閾值（0.15 = 15%）
        """
        self.baseline_threshold = baseline_threshold
        self.baseline_metrics = {}
        self.history = []
    
    def set_baseline(self, metrics: Dict[str, float], version: str = "v1.0"):
        """
        設定基準指標
        
        Args:
            metrics: 基準指標字典（例如：平均回應時間、準確率等）
            version: 模型版本
        """
        self.baseline_metrics = {
            "version": version,
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics
        }
        logger.info(f"設定基準線 - 版本: {version}, 指標: {metrics}")
    
    def check_drift(self, current_metrics: Dict[str, float], version: str = "current") -> Dict:
        """
        檢查當前指標是否偏離基準
        
        Args:
            current_metrics: 當前指標字典
            version: 當前模型版本
            
        Returns:
            漂移檢測結果
        """
        if not self.baseline_metrics:
            return {
                "has_drift": False,
                "error": "尚未設定基準線",
                "recommendation": "請先使用 set_baseline() 設定基準"
            }
        
        results = {
            "version": version,
            "timestamp": datetime.now().isoformat(),
            "has_drift": False,
            "overall_drift_detected": False,  # 別名，方便測試
            "drift_details": {},
            "severity": "none",  # none, low, medium, high, critical
            "drifted_metrics": []
        }
        
        baseline = self.baseline_metrics["metrics"]
        drift_scores = []
        
        # 比較每個指標
        for metric_name, current_value in current_metrics.items():
            if metric_name in baseline:
                baseline_value = baseline[metric_name]
                
                # 計算相對變化率
                if baseline_value != 0:
                    drift_ratio = abs(current_value - baseline_value) / baseline_value
                else:
                    drift_ratio = abs(current_value)
                
                results["drift_details"][metric_name] = {
                    "baseline": baseline_value,
                    "current": current_value,
                    "drift_ratio": drift_ratio,
                    "drift_percentage": f"{drift_ratio * 100:.2f}%",
                    "exceeded_threshold": drift_ratio > self.baseline_threshold
                }
                
                # 記錄是否超過閾值
                if drift_ratio > self.baseline_threshold:
                    results["has_drift"] = True
                    results["overall_drift_detected"] = True
                    results["drifted_metrics"].append(metric_name)
                    drift_scores.append(drift_ratio)
        
        # 判斷嚴重程度
        if drift_scores:
            max_drift = max(drift_scores)
            avg_drift = statistics.mean(drift_scores)
            
            if max_drift > 0.5 or avg_drift > 0.3:
                results["severity"] = "critical"
            elif max_drift > 0.3 or avg_drift > 0.2:
                results["severity"] = "high"
            elif max_drift > 0.2 or avg_drift > 0.15:
                results["severity"] = "medium"
            elif results["has_drift"]:
                results["severity"] = "low"
        
        # 記錄歷史
        self.history.append(results)
        
        logger.info(f"漂移檢測 - 版本: {version}, 有漂移: {results['has_drift']}, "
                   f"嚴重度: {results['severity']}")
        
        return results
    
    def track_metric_over_time(self, metric_name: str, value: float, timestamp: Optional[str] = None):
        """
        追蹤單個指標隨時間的變化
        
        Args:
            metric_name: 指標名稱
            value: 指標值
            timestamp: 時間戳（可選）
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        record = {
            "metric": metric_name,
            "value": value,
            "timestamp": timestamp
        }
        
        self.history.append(record)
        logger.debug(f"追蹤指標 - {metric_name}: {value} @ {timestamp}")
    
    def get_drift_trend(self, metric_name: str, window_size: int = 10) -> Dict:
        """
        分析特定指標的漂移趨勢
        
        Args:
            metric_name: 要分析的指標名稱
            window_size: 分析窗口大小（最近 N 筆記錄）
            
        Returns:
            趨勢分析結果
        """
        # 從歷史記錄中提取指定指標
        metric_history = [
            record for record in self.history 
            if isinstance(record, dict) and 
            record.get("metric") == metric_name
        ]
        
        if len(metric_history) < 2:
            return {
                "metric": metric_name,
                "trend": "unknown",
                "trend_direction": "unknown",  # 測試需要這個鍵
                "message": "沒有足夠的歷史數據",
                "data_points": len(metric_history)
            }
        
        # 取最近的記錄
        recent_records = metric_history[-window_size:]
        values = [record["value"] for record in recent_records]
        
        # 分析趨勢
        if len(values) < 2:
            trend = "stable"
        else:
            # 簡單的線性趨勢檢測
            increasing = sum(1 for i in range(1, len(values)) 
                           if values[i] > values[i-1])
            
            if increasing > len(values) * 0.7:
                trend = "increasing"  # 指標增加
            elif increasing < len(values) * 0.3:
                trend = "decreasing"  # 指標減少
            else:
                trend = "fluctuating"  # 波動
        
        return {
            "metric": metric_name,
            "trend": trend,
            "trend_direction": trend,  # 測試需要這個鍵
            "recent_values": values,
            "data_points": len(values),
            "average": statistics.mean(values),
            "max": max(values),
            "min": min(values)
        }
    
    def generate_drift_report(self) -> Dict:
        """
        生成完整的漂移報告
        
        Returns:
            漂移報告字典
        """
        if not self.baseline_metrics:
            return {"error": "尚未設定基準線"}
        
        report = {
            "baseline": self.baseline_metrics,
            "total_checks": len([h for h in self.history if "has_drift" in h]),
            "drift_detected_count": len([h for h in self.history if h.get("has_drift")]),
            "severity_breakdown": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "none": 0
            },
            "most_drifted_metrics": {},
            "recommendations": []
        }
        
        # 統計嚴重度分布
        for record in self.history:
            if "severity" in record:
                severity = record["severity"]
                report["severity_breakdown"][severity] += 1
        
        # 找出最常漂移的指標
        drift_counts = {}
        for record in self.history:
            if "drifted_metrics" in record:
                for metric in record["drifted_metrics"]:
                    drift_counts[metric] = drift_counts.get(metric, 0) + 1
        
        report["most_drifted_metrics"] = dict(
            sorted(drift_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        )
        
        # 生成建議
        if report["severity_breakdown"]["critical"] > 0:
            report["recommendations"].append("⚠️ 檢測到嚴重漂移，建議立即檢查模型")
        if report["severity_breakdown"]["high"] > 2:
            report["recommendations"].append("⚠️ 多次檢測到高程度漂移，建議進行模型重新訓練")
        if report["drift_detected_count"] / max(report["total_checks"], 1) > 0.5:
            report["recommendations"].append("⚠️ 超過 50% 的檢查發現漂移，建議調整基準線或模型")
        
        if not report["recommendations"]:
            report["recommendations"].append("✅ 模型表現穩定，無明顯漂移")
        
        return report
    
    def reset_history(self):
        """清空歷史記錄"""
        self.history = []
        logger.info("已清空漂移監控歷史記錄")
