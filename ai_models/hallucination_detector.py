"""
HallucinationDetector - AI 幻覺檢測器
檢測 AI 是否產生虛構或不準確的資訊
"""
from typing import Dict, List, Optional, Set
import re
import logging

logger = logging.getLogger(__name__)


class HallucinationDetector:
    """AI 幻覺檢測器 - 檢測 AI 產生的虛構資訊"""
    
    def __init__(self):
        """初始化幻覺檢測器"""
        # 高風險幻覺指標詞彙
        self.confidence_indicators = {
            "high": ["確定", "肯定", "一定", "必須", "絕對", "definitely", "certainly", "must"],
            "low": ["可能", "也許", "大概", "似乎", "probably", "maybe", "might", "perhaps"]
        }
        
        # 事實性聲明的模式
        self.factual_patterns = [
            r'\d{4}年',  # 具體年份
            r'根據.*研究',  # 引用研究
            r'數據顯示',  # 引用數據
            r'\d+%',  # 具體百分比
            r'據.*報導',  # 引用報導
        ]
    
    def detect_hallucination(self, 
                            response: str,
                            known_facts: Optional[List[str]] = None,
                            context: Optional[str] = None) -> Dict:
        """
        綜合檢測幻覺
        
        Args:
            response: AI 回應文字
            known_facts: 已知的事實列表
            context: 原始上下文
            
        Returns:
            檢測結果字典
        """
        results = {
            "response": response,
            "has_hallucination": False,
            "hallucination_risk": "low",  # low, medium, high
            "confidence_score": 0.0,
            "inconsistencies": [],
            "unsupported_claims": [],
            "warnings": []
        }
        
        # 1. 檢查過度自信的聲明
        confidence_analysis = self._analyze_confidence(response)
        if confidence_analysis["high_confidence_count"] > 3:
            results["warnings"].append("回應包含多個高度自信的聲明，可能存在幻覺風險")
            results["hallucination_risk"] = "medium"
        
        # 2. 檢查是否有未支持的事實性聲明
        unsupported = self._detect_unsupported_claims(response, known_facts)
        if unsupported:
            results["unsupported_claims"] = unsupported
            results["hallucination_risk"] = "high"
            results["has_hallucination"] = True
        
        # 3. 檢查內部一致性
        inconsistencies = self._check_internal_consistency(response)
        if inconsistencies:
            results["inconsistencies"] = inconsistencies
            results["hallucination_risk"] = "high"
            results["has_hallucination"] = True
        
        # 4. 檢查與上下文的一致性
        if context:
            context_conflicts = self._check_context_consistency(response, context)
            if context_conflicts:
                results["inconsistencies"].extend(context_conflicts)
                results["hallucination_risk"] = "high"
                results["has_hallucination"] = True
        
        # 計算信心分數（越高越可能不是幻覺）
        risk_levels = {"low": 0.9, "medium": 0.6, "high": 0.3}
        results["confidence_score"] = risk_levels[results["hallucination_risk"]]
        
        logger.info(f"幻覺檢測完成 - 風險: {results['hallucination_risk']}, "
                   f"信心分數: {results['confidence_score']:.2f}")
        
        return results
    
    def _analyze_confidence(self, text: str) -> Dict:
        """
        分析文字中的信心程度指標
        
        Args:
            text: 要分析的文字
            
        Returns:
            信心分析結果
        """
        text_lower = text.lower()
        
        high_count = sum(
            text_lower.count(indicator) 
            for indicator in self.confidence_indicators["high"]
        )
        
        low_count = sum(
            text_lower.count(indicator) 
            for indicator in self.confidence_indicators["low"]
        )
        
        return {
            "high_confidence_count": high_count,
            "low_confidence_count": low_count,
            "confidence_ratio": high_count / (low_count + 1)  # 避免除以零
        }
    
    def _detect_unsupported_claims(self, 
                                   response: str, 
                                   known_facts: Optional[List[str]]) -> List[str]:
        """
        檢測未經支持的事實性聲明
        
        Args:
            response: AI 回應
            known_facts: 已知事實列表
            
        Returns:
            未支持的聲明列表
        """
        unsupported = []
        
        # 尋找事實性聲明模式
        for pattern in self.factual_patterns:
            matches = re.finditer(pattern, response)
            for match in matches:
                claim = match.group()
                
                # 如果提供了已知事實，檢查是否被支持
                if known_facts:
                    is_supported = any(
                        claim in fact or fact in response[max(0, match.start()-50):match.end()+50]
                        for fact in known_facts
                    )
                    
                    if not is_supported:
                        context = response[max(0, match.start()-30):min(len(response), match.end()+30)]
                        unsupported.append(f"未支持的聲明: {context}")
                else:
                    # 沒有提供事實列表，標記為需要驗證
                    context = response[max(0, match.start()-30):min(len(response), match.end()+30)]
                    unsupported.append(f"需要驗證: {context}")
        
        return unsupported
    
    def _check_internal_consistency(self, text: str) -> List[str]:
        """
        檢查文字內部的一致性（例如前後矛盾）
        
        Args:
            text: 要檢查的文字
            
        Returns:
            發現的不一致之處
        """
        inconsistencies = []
        
        # 簡單的矛盾檢測：尋找否定詞後跟肯定詞
        contradiction_patterns = [
            (r'不是.*但.*是', "前後陳述矛盾"),
            (r'沒有.*然而.*有', "存在性陳述矛盾"),
            (r'不會.*卻.*會', "行為陳述矛盾"),
        ]
        
        for pattern, description in contradiction_patterns:
            if re.search(pattern, text):
                inconsistencies.append(f"{description}: 在文本中檢測到矛盾表述")
        
        return inconsistencies
    
    def _check_context_consistency(self, response: str, context: str) -> List[str]:
        """
        檢查回應與上下文的一致性
        
        Args:
            response: AI 回應
            context: 原始上下文
            
        Returns:
            發現的衝突
        """
        conflicts = []
        
        # 提取上下文中的關鍵資訊（數字、日期、名稱等）
        context_numbers = set(re.findall(r'\d+', context))
        response_numbers = set(re.findall(r'\d+', response))
        
        # 檢查是否出現了上下文中沒有的數字（可能是編造的）
        new_numbers = response_numbers - context_numbers
        if len(new_numbers) > 3:  # 允許一些合理的新數字
            conflicts.append(f"回應中出現多個上下文未提及的數字: {list(new_numbers)[:3]}")
        
        return conflicts
    
    def check_for_specific_hallucinations(self, response: str, category: str) -> Dict:
        """
        檢查特定類別的幻覺
        
        Args:
            response: AI 回應
            category: 幻覺類別 (dates, numbers, names, citations)
            
        Returns:
            特定類別的檢測結果
        """
        results = {
            "category": category,
            "issues_found": [],
            "risk_level": "low"
        }
        
        if category == "dates":
            # 檢查日期的合理性
            dates = re.findall(r'\d{4}年', response)
            for date in dates:
                year = int(date[:-1])
                if year < 1900 or year > 2100:
                    results["issues_found"].append(f"不合理的年份: {date}")
                    results["risk_level"] = "high"
        
        elif category == "numbers":
            # 檢查數字的精確性（過於精確可能是編造的）
            precise_numbers = re.findall(r'\d{3,}', response)
            if len(precise_numbers) > 5:
                results["issues_found"].append("包含過多精確數字，可能不可靠")
                results["risk_level"] = "medium"
        
        elif category == "citations":
            # 檢查引用來源
            citations = re.findall(r'根據.*?[，。]', response)
            if not citations and any(pattern in response for pattern in ['研究顯示', '數據表明', '報告指出']):
                results["issues_found"].append("提及研究或數據但未提供具體來源")
                results["risk_level"] = "medium"
        
        return results
