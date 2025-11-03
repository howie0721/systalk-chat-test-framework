"""
AI 回應品質測試
測試 AI 回應的準確性、相關性、完整性等
"""

import pytest
from ai_models.response_evaluator import ResponseEvaluator
from ai_models.hallucination_detector import HallucinationDetector
from ai_models.drift_monitor import DriftMonitor
from ai_models.bias_detector import BiasDetector


class TestResponseQuality:
    """AI 回應品質測試類"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """初始化測試工具"""
        self.evaluator = ResponseEvaluator(min_length=20, max_length=500)
        self.hallucination_detector = HallucinationDetector()
        self.bias_detector = BiasDetector()

    @pytest.mark.ai_quality
    def test_response_accuracy(self):
        """TC-AI-0001: 測試回應準確性 - 應該包含關鍵字且相關"""
        # 模擬場景：詢問 Python 資料類型
        context = "Python 的基本資料類型有哪些？"
        response = "Python 的基本資料類型包括整數（int）、浮點數（float）、字串（str）、布林值（bool）、列表（list）、元組（tuple）、集合（set）和字典（dict）。"
        expected_keywords = ["int", "str", "list", "dict"]

        result = self.evaluator.evaluate_response(response, expected_keywords, context)

        # 驗證
        assert result["passed"], "回應應該通過品質檢查"
        assert result["scores"]["overall"] >= 0.7, "整體分數應該至少 0.7"
        assert result["scores"]["keywords"] >= 0.75, "應該包含至少 75% 的關鍵字"
        print(f"✅ 準確性測試通過 - 整體分數: {result['scores']['overall']:.2f}")

    @pytest.mark.ai_quality
    def test_response_relevance(self):
        """TC-AI-0002: 測試回應相關性 - 應該與問題相關"""
        context = "如何在 Python 中處理異常？"
        relevant_response = (
            "在 Python 中使用 try-except 語句處理異常。將可能拋出異常的代碼放在 try 區塊中，在 except 區塊捕獲並處理異常。"
        )

        result = self.evaluator.evaluate_response(relevant_response, ["try", "except", "異常"], context)

        # 相關的回應應該有相對高的相關性分數（實際演算法可能給出較保守的分數）
        assert result["scores"]["relevance"] >= 0.3, "相關性分數應該至少 0.3"

        # 測試不相關的回應
        irrelevant_response = "今天天氣真好，我喜歡吃冰淇淋。"
        result2 = self.evaluator.evaluate_response(irrelevant_response, ["try", "except"], context)

        # 不相關的回應應該有低相關性分數
        assert result2["scores"]["relevance"] < result["scores"]["relevance"], "不相關回應的相關性分數應該更低"
        print(f"✅ 相關性測試通過 - 相關: {result['scores']['relevance']:.2f}, 不相關: {result2['scores']['relevance']:.2f}")

    @pytest.mark.ai_quality
    def test_response_completeness(self):
        """測試回應完整性 - 不應該被截斷或不完整"""
        # 完整的回應
        complete_response = "機器學習是人工智慧的一個分支，它使用數據和算法來模仿人類學習的方式。"
        result = self.evaluator.evaluate_response(complete_response, [], "")

        assert result["scores"]["completeness"] >= 0.8, "完整回應的完整性分數應該至少 0.8"

        # 不完整的回應
        incomplete_response = "機器學習是..."
        result2 = self.evaluator.evaluate_response(incomplete_response, [], "")

        # 不完整的回應應該有較低的分數（"..." 會被扣分）
        assert result2["scores"]["completeness"] < result["scores"]["completeness"], "不完整回應的完整性分數應該較低"
        print(
            f"✅ 完整性測試通過 - 完整: {result['scores']['completeness']:.2f}, 不完整: {result2['scores']['completeness']:.2f}"
        )

    @pytest.mark.ai_quality
    def test_no_hallucination(self):
        """測試無幻覺 - 回應不應該包含捏造的事實"""
        # 正常回應
        normal_response = "Python 是一種高階程式語言，由 Guido van Rossum 創建。"
        context = "介紹 Python 程式語言"
        known_facts = ["Python", "Guido van Rossum", "高階", "程式語言"]

        result = self.hallucination_detector.detect_hallucination(normal_response, known_facts, context)

        assert not result["has_hallucination"] or result["risk_level"] == "low", "正常回應不應該有高風險幻覺"

        # 包含可疑事實的回應（測試檢測能力）
        suspicious_response = "根據 2025 年的 XYZ 研究報告，100% 的開發者都認為..."
        result2 = self.hallucination_detector.detect_hallucination(suspicious_response, [], context)

        # 應該檢測到未支持的聲明
        assert len(result2["unsupported_claims"]) > 0, "應該檢測到未支持的聲明"
        print(f"✅ 幻覺檢測測試通過")

    @pytest.mark.ai_quality
    def test_response_length_appropriate(self):
        """測試回應長度適當性"""
        # 太短的回應
        too_short = "好"
        result = self.evaluator.evaluate_response(too_short, [], "")
        assert result["scores"]["length"] < 0.5, "太短的回應長度分數應該較低"

        # 適當長度的回應（需要至少 20 字元，這裡中文約 30 字元）
        appropriate = "這是一個適當長度的回應，包含了充分的信息來回答問題。雖然簡潔但有足夠的內容。"
        result2 = self.evaluator.evaluate_response(appropriate, [], "")
        assert result2["scores"]["length"] > result["scores"]["length"], "適當長度的回應長度分數應該較高"

        print(f"✅ 長度適當性測試通過 - 太短: {result['scores']['length']:.2f}, 適當: {result2['scores']['length']:.2f}")

    @pytest.mark.ai_quality
    def test_no_bias(self):
        """測試無偏見 - 回應應該公平公正"""
        # 公平的回應
        fair_response = "軟體工程師需要具備邏輯思維、解決問題的能力和團隊合作精神。"
        result = self.bias_detector.detect_bias(fair_response, categories=["gender", "age"])

        assert result["fairness_score"] >= 0.8, "公平回應的公平性分數應該至少 0.8"

        # 可能有偏見的回應
        biased_response = "所有女性都比較感性，男性總是比較理性，這是天生的差異。"
        result2 = self.bias_detector.detect_bias(biased_response, categories=["gender"])

        assert result2["has_bias"], "應該檢測到性別偏見"
        assert result2["fairness_score"] < 0.7, "有偏見回應的公平性分數應該較低"
        print(f"✅ 偏見檢測測試通過")

    @pytest.mark.ai_quality
    def test_error_response_detection(self):
        """測試錯誤回應檢測 - 應該能識別錯誤狀態"""
        error_responses = ["", "Error: Connection timeout", "系統錯誤", "無法回答此問題"]

        for error_resp in error_responses:
            is_error = self.evaluator.is_empty_or_error_response(error_resp)
            assert is_error, f"應該識別出錯誤回應: {error_resp}"

        # 正常回應不應該被誤判為錯誤
        normal_response = "這是一個正常的回應，包含有用的信息。"
        assert not self.evaluator.is_empty_or_error_response(normal_response), "正常回應不應該被誤判為錯誤"

        print(f"✅ 錯誤回應檢測測試通過")


class TestModelDrift:
    """模型漂移測試類"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """初始化漂移監控器"""
        self.drift_monitor = DriftMonitor(baseline_threshold=0.15)

    @pytest.mark.ai_quality
    def test_drift_detection_stable_model(self):
        """測試穩定模型 - 不應該檢測到漂移"""
        # 設定基準
        baseline_metrics = {"response_time": 1.2, "accuracy": 0.85, "completeness": 0.90}
        self.drift_monitor.set_baseline(baseline_metrics, version="v1.0")

        # 當前指標（變化小於 15%）
        current_metrics = {"response_time": 1.25, "accuracy": 0.86, "completeness": 0.89}  # +4%  # +1%  # -1%

        result = self.drift_monitor.check_drift(current_metrics, version="v1.0")

        # 不應該有嚴重漂移
        assert result["overall_drift_detected"] == False, "穩定模型不應該檢測到整體漂移"
        print(f"✅ 穩定模型測試通過")

    @pytest.mark.ai_quality
    def test_drift_detection_degraded_model(self):
        """測試退化模型 - 應該檢測到漂移"""
        # 設定基準
        baseline_metrics = {"response_time": 1.0, "accuracy": 0.85, "completeness": 0.90}
        self.drift_monitor.set_baseline(baseline_metrics, version="v1.0")

        # 當前指標（顯著變化）
        current_metrics = {"response_time": 2.5, "accuracy": 0.70, "completeness": 0.75}  # +150%  # -17.6%  # -16.7%

        result = self.drift_monitor.check_drift(current_metrics, version="v1.1")

        # 應該檢測到漂移
        assert result["overall_drift_detected"], "退化模型應該檢測到整體漂移"
        assert len(result["drifted_metrics"]) >= 2, "應該檢測到多個指標漂移"

        # 檢查嚴重程度
        severity = result["severity"]
        assert severity in ["medium", "high", "critical"], f"退化模型的嚴重程度應該至少是 medium，實際: {severity}"

        print(f"✅ 退化模型測試通過 - 嚴重程度: {severity}")

    @pytest.mark.ai_quality
    def test_metric_tracking_over_time(self):
        """測試時間序列追蹤"""
        import time

        # 追蹤指標
        for i in range(5):
            self.drift_monitor.track_metric_over_time("accuracy", 0.85 + i * 0.01)
            time.sleep(0.01)  # 確保時間戳不同

        # 獲取趨勢
        trend = self.drift_monitor.get_drift_trend("accuracy")

        assert "trend_direction" in trend, "應該返回趨勢方向"
        assert trend["data_points"] == 5, "應該有 5 個數據點"

        print(f"✅ 時間序列追蹤測試通過 - 趨勢: {trend['trend_direction']}")


class TestComparativeAnalysis:
    """比較分析測試類"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """初始化測試工具"""
        self.evaluator = ResponseEvaluator()
        self.bias_detector = BiasDetector()

    @pytest.mark.ai_quality
    def test_ab_testing(self):
        """測試 A/B 測試功能 - 比較兩個回應"""
        response_a = "Python 是一種易學易用的程式語言，適合初學者。它有豐富的函式庫和活躍的社群支持。"
        response_b = "Python 是程式語言。"

        comparison = self.evaluator.compare_responses(response_a, response_b)

        # Response A 應該更好（或至少不會更差）
        assert "better_response" in comparison
        assert comparison["better_response"] in ["response1", "equal"], "更詳細完整的回應應該被評為更好或相等"
        assert comparison["response1_score"] >= comparison["response2_score"], "Response A 的分數應該高於或等於 Response B"

        print(
            f"✅ A/B 測試通過 - 更好的回應: {comparison['better_response']} (A:{comparison['response1_score']:.2f}, B:{comparison['response2_score']:.2f})"
        )

    @pytest.mark.ai_quality
    def test_fairness_comparison(self):
        """測試公平性比較"""
        response1 = "工程師需要邏輯思維和技術能力。"
        response2 = "男性工程師總是比女性工程師更理性。"

        comparison = self.bias_detector.compare_fairness(response1, response2)

        # Response 1 應該更公平
        assert comparison["fairer_response"] == "response1", "無偏見的回應應該被評為更公平"
        assert comparison["response1_fairness"] > comparison["response2_fairness"], "公平性分數應該反映實際差異"

        print(f"✅ 公平性比較測試通過")


@pytest.mark.ai_quality
def test_batch_analysis():
    """測試批量分析功能"""
    bias_detector = BiasDetector()

    # 一批回應
    responses = [
        "軟體開發需要團隊合作。",
        "所有年輕人都不負責任。",  # 有年齡偏見
        "Python 是一種程式語言。",
        "女性總是比較感性。",  # 有性別偏見
        "測試是軟體品質保證的關鍵。",
    ]

    report = bias_detector.generate_fairness_report(responses)

    # 驗證報告結構
    assert report["total_responses"] == 5
    assert report["biased_responses"] >= 2, "應該檢測到至少 2 個有偏見的回應"
    assert "average_fairness_score" in report
    assert "recommendations" in report
    assert len(report["recommendations"]) > 0

    print(f"✅ 批量分析測試通過")
    print(f"   總回應數: {report['total_responses']}")
    print(f"   有偏見回應: {report['biased_responses']}")
    print(f"   平均公平性: {report['average_fairness_score']:.2f}")
