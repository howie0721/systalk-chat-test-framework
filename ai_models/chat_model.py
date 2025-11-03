"""
AI 聊天模型 - 用於測試的 Mock 實作
實際專案中會替換為真實的 LLM API 調用
"""

import time
import random
from typing import Dict, List, Optional


class ChatModel:
    """AI 聊天模型類別"""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.7):
        """
        初始化聊天模型
        
        Args:
            model_name: 模型名稱
            temperature: 溫度參數 (0.0-1.0)
        """
        self.model_name = model_name
        self.temperature = temperature
        self.conversation_history: List[Dict[str, str]] = []
        self._is_initialized = True
        
    def reply(self, prompt: str, context: Optional[Dict] = None) -> str:
        """
        根據 prompt 生成回應
        
        Args:
            prompt: 用戶輸入的提示詞
            context: 可選的上下文資訊
            
        Returns:
            模型的回應文本
        """
        if not prompt or not prompt.strip():
            return "請輸入有效的內容"
        
        # 模擬處理時間
        time.sleep(0.01)
        
        # 記錄對話歷史
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        # 根據 prompt 生成回應 (Mock 實作)
        response = self._generate_response(prompt, context)
        
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        return response
    
    def _generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        """生成回應的內部邏輯 (Mock)"""
        prompt_lower = prompt.lower()
        
        # 問候語
        if any(word in prompt_lower for word in ["你好", "hello", "hi", "嗨"]):
            return "你好！我是 SysTalk.Chat AI 助手，很高興為您服務。有什麼我可以幫助您的嗎？"
        
        # 帳戶相關
        if "帳戶" in prompt_lower or "餘額" in prompt_lower:
            return "您的帳戶餘額為 NT$10,000。如需更詳細的交易記錄，請告訴我您想查詢的時間範圍。"
        
        # 天氣查詢
        if "天氣" in prompt_lower:
            return "今天台北市天氣晴朗，溫度約 25°C，適合外出活動。"
        
        # 空輸入處理
        if not prompt.strip():
            return "請輸入有效的內容"
        
        # 預設回應
        return f"我理解您的問題：「{prompt}」。這是一個很好的問題，讓我為您提供相關資訊..."
    
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        多輪對話介面
        
        Args:
            messages: 對話訊息列表 [{"role": "user", "content": "..."}]
            
        Returns:
            模型回應
        """
        if not messages:
            return "沒有接收到任何訊息"
        
        last_message = messages[-1]
        return self.reply(last_message.get("content", ""))
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """獲取對話歷史"""
        return self.conversation_history.copy()
    
    def clear_history(self):
        """清空對話歷史"""
        self.conversation_history.clear()
    
    def is_initialized(self) -> bool:
        """檢查模型是否已初始化"""
        return self._is_initialized
    
    def get_model_info(self) -> Dict[str, any]:
        """獲取模型資訊"""
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "conversation_length": len(self.conversation_history)
        }
    
    def validate_input(self, prompt: str) -> bool:
        """
        驗證輸入是否合法
        
        Returns:
            True: 合法, False: 不合法
        """
        if not prompt:
            return False
        if len(prompt.strip()) == 0:
            return False
        if len(prompt) > 4000:  # 超過長度限制
            return False
        return True
    
    def estimate_tokens(self, text: str) -> int:
        """
        估算文本的 token 數量 (簡化版)
        
        Args:
            text: 輸入文本
            
        Returns:
            估算的 token 數量
        """
        # 簡化計算：中文約 2 字符/token，英文約 4 字符/token
        chinese_chars = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
        other_chars = len(text) - chinese_chars
        
        tokens = (chinese_chars // 2) + (other_chars // 4)
        return max(1, tokens)
