"""
ResponseEvaluator - AI 回應品質評估器
評估 AI 回應的品質（相關性、完整性、準確性）
"""

from typing import Dict, List, Optional
import re
from difflib import SequenceMatcher
import logging

logger = logging.getLogger(__name__)


class ResponseEvaluator:
    """AI 回應品質評估器"""

    def __init__(self, min_length: int = 10, max_length: int = 1000):
        """
        初始化評估器

        Args:
            min_length: 最小回應長度
            max_length: 最大回應長度
        """
        self.min_length = min_length
        self.max_length = max_length

    def evaluate_response(
        self, response: str, expected_keywords: Optional[List[str]] = None, context: Optional[str] = None
    ) -> Dict:
        """
        綜合評估回應品質

        Args:
            response: AI 回應文字
            expected_keywords: 預期應包含的關鍵詞列表
            context: 原始問題或上下文

        Returns:
            評估結果字典
        """
        results = {
            "response": response,
            "length_score": self.evaluate_length(response),
            "completeness_score": self.evaluate_completeness(response),
            "keyword_score": 0.0,
            "relevance_score": 0.0,
            "overall_score": 0.0,
            "passed": False,
            "issues": [],
        }

        # 關鍵詞評估
        if expected_keywords:
            results["keyword_score"] = self.evaluate_keywords(response, expected_keywords)
            if results["keyword_score"] < 0.5:
                results["issues"].append(f"缺少預期關鍵詞（分數：{results['keyword_score']:.2f}）")

        # 相關性評估（如果有上下文）
        if context:
            results["relevance_score"] = self.evaluate_relevance(response, context)
            if results["relevance_score"] < 0.3:
                results["issues"].append(f"回應與問題相關性低（分數：{results['relevance_score']:.2f}）")

        # 計算總分
        scores = [
            results["length_score"],
            results["completeness_score"],
            results["keyword_score"] if expected_keywords else 1.0,
            results["relevance_score"] if context else 1.0,
        ]
        results["overall_score"] = sum(scores) / len(scores)

        # 組織分數結構（為測試提供統一介面）
        results["scores"] = {
            "overall": results["overall_score"],
            "length": results["length_score"],
            "completeness": results["completeness_score"],
            "keywords": results["keyword_score"],
            "relevance": results["relevance_score"],
        }

        # 判斷是否通過（總分 >= 0.6 且無嚴重問題）
        results["passed"] = results["overall_score"] >= 0.6 and len(results["issues"]) == 0

        logger.info(f"回應評估完成 - 總分: {results['overall_score']:.2f}, 通過: {results['passed']}")

        return results

    def evaluate_length(self, response: str) -> float:
        """
        評估回應長度是否合適

        Args:
            response: AI 回應文字

        Returns:
            長度分數 (0.0-1.0)
        """
        length = len(response.strip())

        if length < self.min_length:
            return 0.0
        elif length > self.max_length:
            return 0.5  # 過長扣分但不完全失敗
        else:
            # 在合理範圍內，根據與理想長度的接近度評分
            ideal_length = (self.min_length + self.max_length) / 2
            distance = abs(length - ideal_length) / ideal_length
            return max(0.5, 1.0 - distance)

    def evaluate_completeness(self, response: str) -> float:
        """
        評估回應的完整性

        Args:
            response: AI 回應文字

        Returns:
            完整性分數 (0.0-1.0)
        """
        score = 1.0
        response_lower = response.lower().strip()

        # 檢查是否有不完整的跡象
        incomplete_indicators = ["...", "[未完成]", "[待續]", "無法回答", "不知道", "沒有資訊"]

        for indicator in incomplete_indicators:
            if indicator in response_lower:
                score -= 0.3

        # 檢查是否有句子結束符號
        if not re.search(r"[。！？.!?]$", response.strip()):
            score -= 0.2

        return max(0.0, score)

    def evaluate_keywords(self, response: str, keywords: List[str]) -> float:
        """
        評估回應是否包含預期關鍵詞

        Args:
            response: AI 回應文字
            keywords: 預期關鍵詞列表

        Returns:
            關鍵詞涵蓋率 (0.0-1.0)
        """
        if not keywords:
            return 1.0

        response_lower = response.lower()
        found_keywords = sum(1 for kw in keywords if kw.lower() in response_lower)
        coverage = found_keywords / len(keywords)

        logger.debug(f"關鍵詞覆蓋率: {found_keywords}/{len(keywords)} = {coverage:.2f}")

        return coverage

    def evaluate_relevance(self, response: str, context: str) -> float:
        """
        評估回應與上下文的相關性（使用簡單的字串相似度）

        Args:
            response: AI 回應文字
            context: 原始問題或上下文

        Returns:
            相關性分數 (0.0-1.0)
        """

        # 提取有意義的詞彙（移除停用詞）
        def extract_meaningful_words(text: str) -> set:
            # 簡單的停用詞列表
            stop_words = {
                "的",
                "是",
                "在",
                "了",
                "和",
                "有",
                "我",
                "你",
                "他",
                "她",
                "它",
                "the",
                "is",
                "in",
                "and",
                "of",
                "a",
                "to",
                "for",
            }
            words = set(re.findall(r"\w+", text.lower()))
            return words - stop_words

        response_words = extract_meaningful_words(response)
        context_words = extract_meaningful_words(context)

        if not context_words:
            return 0.5  # 無法判斷，給中等分數

        # 計算詞彙重疊率
        overlap = len(response_words & context_words)
        relevance = overlap / len(context_words)

        # 也考慮整體字串相似度
        similarity = SequenceMatcher(None, response.lower(), context.lower()).ratio()

        # 綜合評分（詞彙重疊占 70%，字串相似度占 30%）
        final_score = 0.7 * min(relevance, 1.0) + 0.3 * similarity

        logger.debug(f"相關性評估 - 詞彙重疊: {overlap}, 相似度: {similarity:.2f}, 最終: {final_score:.2f}")

        return final_score

    def compare_responses(self, response1: str, response2: str) -> Dict:
        """
        比較兩個回應的質量（用於 A/B 測試或回歸測試）

        Args:
            response1: 第一個回應
            response2: 第二個回應

        Returns:
            比較結果字典
        """
        eval1 = self.evaluate_response(response1, [], "")
        eval2 = self.evaluate_response(response2, [], "")

        similarity = SequenceMatcher(None, response1, response2).ratio()

        result = {
            "response1_score": eval1["overall_score"],
            "response2_score": eval2["overall_score"],
            "similarity": similarity,
            "better_response": None,
        }

        if eval1["overall_score"] > eval2["overall_score"]:
            result["better_response"] = "response1"
        elif eval2["overall_score"] > eval1["overall_score"]:
            result["better_response"] = "response2"
        else:
            result["better_response"] = "equal"

        return result

    def is_empty_or_error_response(self, response: str) -> bool:
        """
        檢查回應是否為空或錯誤訊息

        Args:
            response: AI 回應文字

        Returns:
            True 如果是空回應或錯誤訊息
        """
        if not response or not response.strip():
            return True

        error_indicators = ["error", "錯誤", "系統異常", "無法處理", "無法回答", "服務暫時不可用", "internal server error"]

        response_lower = response.lower()
        return any(indicator in response_lower for indicator in error_indicators)
