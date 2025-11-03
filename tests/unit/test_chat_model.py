"""AI 聊天模型單元測試"""

import pytest
import time


@pytest.mark.unit
@pytest.mark.smoke
class TestChatModelInitialization:
    """聊天模型初始化測試"""
    
    def test_TC_UNIT_0011_model_initialization(self, chat_model):
        """TC-UNIT-0011: 驗證模型能正確初始化"""
        # Assert
        assert chat_model.is_initialized() is True
        assert chat_model.model_name == "gpt-3.5-turbo"
        assert chat_model.temperature == 0.7
    
    def test_TC_UNIT_0012_model_info(self, chat_model):
        """TC-UNIT-0012: 驗證模型資訊獲取"""
        # Act
        info = chat_model.get_model_info()
        
        # Assert
        assert "model_name" in info
        assert "temperature" in info
        assert "conversation_length" in info
        assert info["model_name"] == "gpt-3.5-turbo"


@pytest.mark.unit
class TestChatModelBasicReplies:
    """聊天模型基本回應測試"""
    
    def test_TC_UNIT_0013_reply_to_greeting(self, chat_model):
        """TC-UNIT-0013: 驗證模型能正確回應問候語"""
        # Arrange
        prompt = "你好"
        
        # Act
        response = chat_model.reply(prompt)
        
        # Assert
        assert response is not None
        assert len(response) > 0
        assert "你好" in response or "Hello" in response
    
    def test_TC_UNIT_0014_reply_to_account_query(self, chat_model):
        """TC-UNIT-0014: 驗證模型能回應帳戶查詢"""
        # Arrange
        prompt = "我想查詢帳戶餘額"
        
        # Act
        response = chat_model.reply(prompt)
        
        # Assert
        assert response is not None
        assert "帳戶" in response or "餘額" in response
    
    def test_TC_UNIT_0015_reply_to_weather_query(self, chat_model):
        """TC-UNIT-0015: 驗證模型能回應天氣查詢"""
        # Arrange
        prompt = "今天台北天氣如何？"
        
        # Act
        response = chat_model.reply(prompt)
        
        # Assert
        assert response is not None
        assert "天氣" in response or "溫度" in response or "晴" in response or "雨" in response


@pytest.mark.unit
class TestChatModelInputValidation:
    """聊天模型輸入驗證測試"""
    
    def test_TC_UNIT_0016_empty_input_handling(self, chat_model):
        """TC-UNIT-0016: 驗證空輸入的處理"""
        # Arrange
        prompt = ""
        
        # Act
        response = chat_model.reply(prompt)
        
        # Assert
        assert response == "請輸入有效的內容"
    
    def test_TC_UNIT_0017_whitespace_input_handling(self, chat_model):
        """TC-UNIT-0017: 驗證純空白輸入的處理"""
        # Arrange
        prompt = "   "
        
        # Act
        response = chat_model.reply(prompt)
        
        # Assert
        assert response == "請輸入有效的內容"
    
    def test_TC_UNIT_0018_input_validation_valid(self, chat_model):
        """TC-UNIT-0018: 驗證合法輸入通過驗證"""
        # Arrange
        prompt = "你好，這是一個正常的問題"
        
        # Act
        is_valid = chat_model.validate_input(prompt)
        
        # Assert
        assert is_valid is True
    
    def test_TC_UNIT_0019_input_validation_empty(self, chat_model):
        """TC-UNIT-0019: 驗證空輸入不通過驗證"""
        # Act
        is_valid_empty = chat_model.validate_input("")
        is_valid_none = chat_model.validate_input(None)
        
        # Assert
        assert is_valid_empty is False
        assert is_valid_none is False
    
    def test_TC_UNIT_0020_input_validation_too_long(self, chat_model):
        """TC-UNIT-0020: 驗證過長輸入不通過驗證"""
        # Arrange
        long_prompt = "x" * 5000  # 超過 4000 字符限制
        
        # Act
        is_valid = chat_model.validate_input(long_prompt)
        
        # Assert
        assert is_valid is False


@pytest.mark.unit
class TestChatModelConversationHistory:
    """聊天模型對話歷史測試"""
    
    def test_TC_UNIT_0021_conversation_history_recording(self, chat_model):
        """TC-UNIT-0021: 驗證對話歷史被正確記錄"""
        # Arrange
        prompt1 = "第一個問題"
        prompt2 = "第二個問題"
        
        # Act
        chat_model.reply(prompt1)
        chat_model.reply(prompt2)
        history = chat_model.get_conversation_history()
        
        # Assert
        assert len(history) == 4  # 2 user + 2 assistant
        assert history[0]["role"] == "user"
        assert history[0]["content"] == prompt1
        assert history[1]["role"] == "assistant"
        assert history[2]["role"] == "user"
        assert history[2]["content"] == prompt2
    
    def test_TC_UNIT_0022_clear_conversation_history(self, chat_model):
        """TC-UNIT-0022: 驗證對話歷史清除功能"""
        # Arrange
        chat_model.reply("測試訊息")
        
        # Act
        chat_model.clear_history()
        history = chat_model.get_conversation_history()
        
        # Assert
        assert len(history) == 0
    
    def test_TC_UNIT_0023_conversation_history_isolation(self, chat_model):
        """TC-UNIT-0023: 驗證對話歷史的隔離性"""
        # Arrange
        chat_model.reply("測試")
        
        # Act
        history1 = chat_model.get_conversation_history()
        history1.append({"role": "hacker", "content": "try to modify"})
        history2 = chat_model.get_conversation_history()
        
        # Assert - 修改副本不應影響原始歷史
        assert len(history1) == 3  # 被修改的副本
        assert len(history2) == 2  # 原始歷史未被影響


@pytest.mark.unit
class TestChatModelMultiRoundChat:
    """聊天模型多輪對話測試"""
    
    def test_TC_UNIT_0024_multi_round_chat_interface(self, chat_model):
        """TC-UNIT-0024: 驗證多輪對話介面"""
        # Arrange
        messages = [
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "你好！有什麼可以幫您的嗎？"},
            {"role": "user", "content": "查詢帳戶餘額"}
        ]
        
        # Act
        response = chat_model.chat(messages)
        
        # Assert
        assert response is not None
        assert len(response) > 0
    
    def test_TC_UNIT_0025_chat_with_empty_messages(self, chat_model):
        """TC-UNIT-0025: 驗證空訊息列表的處理"""
        # Act
        response = chat_model.chat([])
        
        # Assert
        assert response == "沒有接收到任何訊息"


@pytest.mark.unit
class TestChatModelTokenEstimation:
    """聊天模型 Token 估算測試"""
    
    def test_TC_UNIT_0026_token_estimation_english(self, chat_model):
        """TC-UNIT-0026: 驗證英文文本 token 估算"""
        # Arrange
        text = "Hello world"  # 約 11 字符，估算約 2-3 tokens
        
        # Act
        tokens = chat_model.estimate_tokens(text)
        
        # Assert
        assert tokens > 0
        assert tokens < 10  # 合理範圍
    
    def test_TC_UNIT_0027_token_estimation_chinese(self, chat_model):
        """TC-UNIT-0027: 驗證中文文本 token 估算"""
        # Arrange
        text = "你好世界"  # 4 個中文字，估算約 2 tokens
        
        # Act
        tokens = chat_model.estimate_tokens(text)
        
        # Assert
        assert tokens > 0
        assert tokens < 10
    
    def test_TC_UNIT_0028_token_estimation_mixed(self, chat_model):
        """TC-UNIT-0028: 驗證中英混合文本 token 估算"""
        # Arrange
        text = "Hello 你好 World 世界"
        
        # Act
        tokens = chat_model.estimate_tokens(text)
        
        # Assert
        assert tokens > 0


@pytest.mark.unit
@pytest.mark.performance
class TestChatModelPerformance:
    """聊天模型效能單元測試"""
    
    def test_TC_UNIT_0029_response_time(self, chat_model):
        """TC-UNIT-0029: 驗證單次回應時間在合理範圍內"""
        # Arrange
        prompt = "這是一個測試問題"
        
        # Act
        start_time = time.time()
        response = chat_model.reply(prompt)
        end_time = time.time()
        response_time = end_time - start_time
        
        # Assert
        assert response is not None
        assert response_time < 1.0  # 單次回應應小於 1 秒


@pytest.mark.unit
class TestChatModelTemperature:
    """聊天模型溫度參數測試"""
    
    def test_TC_UNIT_0030_low_temperature_model(self, chat_model_low_temp):
        """TC-UNIT-0030: 驗證低溫度模型配置"""
        # Assert
        assert chat_model_low_temp.temperature == 0.1
        assert chat_model_low_temp.is_initialized() is True
        
        # Act
        response = chat_model_low_temp.reply("你好")
        
        # Assert
        assert response is not None
