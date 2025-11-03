"""AI 聊天模型整合測試"""

import pytest
import time


@pytest.mark.integration
class TestChatModelContextIntegration:
    """聊天模型上下文整合測試"""
    
    def test_TC_INTE_0011_multi_turn_conversation_flow(self, chat_model):
        """TC-INTE-0011: 測試多輪對話的完整流程"""
        # Arrange
        prompts = [
            "你好",
            "我想查詢帳戶餘額",
            "謝謝"
        ]
        
        responses = []
        
        # Act
        for prompt in prompts:
            response = chat_model.reply(prompt)
            responses.append(response)
        
        # Assert
        assert len(responses) == 3
        assert all(len(r) > 0 for r in responses)
        
        # 驗證對話歷史完整性
        history = chat_model.get_conversation_history()
        assert len(history) == 6  # 3 user + 3 assistant
    
    def test_TC_INTE_0012_conversation_context_preservation(self, chat_model):
        """TC-INTE-0012: 測試對話上下文保持"""
        # Act - 第一輪對話
        chat_model.reply("我叫張三")
        
        # Act - 第二輪對話（應該能記住上文）
        history = chat_model.get_conversation_history()
        
        # Assert
        assert len(history) == 2
        assert "張三" in history[0]["content"]


@pytest.mark.integration
class TestChatModelWithDifferentInputTypes:
    """聊天模型不同輸入類型整合測試"""
    
    def test_TC_INTE_0013_handle_various_input_scenarios(self, chat_model, sample_prompts):
        """TC-INTE-0013: 測試處理各種輸入場景"""
        # Arrange
        test_cases = [
            (sample_prompts["greeting"], True),
            (sample_prompts["question"], True),
            (sample_prompts["account_query"], True),
            (sample_prompts["empty"], False),  # 應該返回錯誤訊息
        ]
        
        # Act & Assert
        for prompt, should_succeed in test_cases:
            response = chat_model.reply(prompt)
            
            if should_succeed:
                assert len(response) > 0
                assert response != "請輸入有效的內容"
            else:
                assert response == "請輸入有效的內容"
    
    def test_TC_INTE_0014_batch_processing(self, chat_model):
        """TC-INTE-0014: 測試批量處理多個問題"""
        # Arrange
        questions = [
            "問題一：什麼是AI？",
            "問題二：什麼是機器學習？",
            "問題三：什麼是深度學習？"
        ]
        
        # Act
        responses = []
        for question in questions:
            response = chat_model.reply(question)
            responses.append(response)
        
        # Assert
        assert len(responses) == len(questions)
        assert all(len(r) > 0 for r in responses)
        assert all(r != "請輸入有效的內容" for r in responses)


@pytest.mark.integration
class TestChatModelWithConfiguration:
    """聊天模型配置整合測試"""
    
    def test_TC_INTE_0015_model_with_different_temperatures(self):
        """TC-INTE-0015: 測試不同溫度參數的模型"""
        from ai_models.chat_model import ChatModel
        
        # Arrange
        model_high_temp = ChatModel(temperature=0.9)
        model_low_temp = ChatModel(temperature=0.1)
        prompt = "告訴我關於台灣的一些事情"
        
        # Act
        response_high = model_high_temp.reply(prompt)
        response_low = model_low_temp.reply(prompt)
        
        # Assert
        assert response_high is not None
        assert response_low is not None
        assert len(response_high) > 0
        assert len(response_low) > 0
        
        # Cleanup
        model_high_temp.clear_history()
        model_low_temp.clear_history()
    
    def test_TC_INTE_0016_model_initialization_with_config(self, config):
        """TC-INTE-0016: 測試從配置初始化模型"""
        from ai_models.chat_model import ChatModel
        
        # Arrange - 模擬從配置讀取參數
        model_config = {
            "model_name": "gpt-3.5-turbo",
            "temperature": 0.7
        }
        
        # Act
        model = ChatModel(**model_config)
        
        # Assert
        assert model.is_initialized()
        assert model.model_name == model_config["model_name"]
        assert model.temperature == model_config["temperature"]
        
        # Cleanup
        model.clear_history()


@pytest.mark.integration
class TestChatModelEndToEndScenarios:
    """聊天模型端到端場景整合測試"""
    
    def test_TC_INTE_0017_customer_service_scenario(self, chat_model):
        """TC-INTE-0017: 測試客服場景完整流程"""
        # Arrange - 模擬客戶服務對話流程
        conversation_flow = [
            ("你好", ["你好", "Hello"]),
            ("我想查詢帳戶餘額", ["帳戶", "餘額"]),
            ("謝謝你的幫助", ["謝謝", "幫助", "服務"])
        ]
        
        # Act & Assert
        for prompt, expected_keywords in conversation_flow:
            response = chat_model.reply(prompt)
            
            # 驗證回應包含至少一個預期關鍵字
            assert any(keyword in response for keyword in expected_keywords), \
                f"回應「{response}」應包含關鍵字 {expected_keywords} 之一"
    
    def test_TC_INTE_0018_error_recovery_scenario(self, chat_model):
        """TC-INTE-0018: 測試錯誤恢復場景"""
        # Arrange & Act - 先發送錯誤輸入
        error_response = chat_model.reply("")
        
        # Assert - 確認錯誤被正確處理
        assert error_response == "請輸入有效的內容"
        
        # Act - 再發送正常輸入，模型應該能恢復
        normal_response = chat_model.reply("現在我想正常提問")
        
        # Assert - 確認模型已恢復正常
        assert normal_response != "請輸入有效的內容"
        assert len(normal_response) > 0
    
    def test_TC_INTE_0019_session_lifecycle(self, chat_model):
        """TC-INTE-0019: 測試會話生命週期"""
        # Act - 階段 1: 開始對話
        chat_model.reply("開始對話")
        assert len(chat_model.get_conversation_history()) == 2
        
        # Act - 階段 2: 繼續對話
        chat_model.reply("繼續對話")
        assert len(chat_model.get_conversation_history()) == 4
        
        # Act - 階段 3: 清除並重新開始
        chat_model.clear_history()
        assert len(chat_model.get_conversation_history()) == 0
        
        # Act - 階段 4: 新會話
        chat_model.reply("新的對話")
        assert len(chat_model.get_conversation_history()) == 2


@pytest.mark.integration
@pytest.mark.performance
class TestChatModelPerformanceIntegration:
    """聊天模型效能整合測試"""
    
    def test_TC_INTE_0020_concurrent_conversations_simulation(self, chat_model):
        """TC-INTE-0020: 測試模擬並發對話（單執行緒順序執行）"""
        # Arrange
        num_conversations = 10
        
        # Act
        start_time = time.time()
        for i in range(num_conversations):
            response = chat_model.reply(f"這是第 {i+1} 個問題")
            assert response is not None
        end_time = time.time()
        
        total_time = end_time - start_time
        avg_time = total_time / num_conversations
        
        # Assert
        assert avg_time < 0.5  # 平均每個回應應小於 0.5 秒
    
    def test_TC_INTE_0021_sustained_load_test(self, chat_model):
        """TC-INTE-0021: 測試持續負載"""
        # Arrange
        num_requests = 50
        max_acceptable_time = 30  # 50 個請求應在 30 秒內完成
        
        # Act
        start_time = time.time()
        success_count = 0
        
        for i in range(num_requests):
            try:
                response = chat_model.reply(f"負載測試問題 {i}")
                if response and response != "請輸入有效的內容":
                    success_count += 1
            except Exception:
                pass
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Assert
        assert total_time < max_acceptable_time
        assert success_count >= num_requests * 0.95  # 95% 成功率


@pytest.mark.integration
class TestChatModelDataPersistence:
    """聊天模型數據持久化整合測試"""
    
    def test_TC_INTE_0022_conversation_history_integrity(self, chat_model):
        """TC-INTE-0022: 測試對話歷史完整性"""
        # Arrange
        messages = ["訊息1", "訊息2", "訊息3"]
        
        # Act
        for msg in messages:
            chat_model.reply(msg)
        
        history = chat_model.get_conversation_history()
        
        # Assert - 驗證所有訊息都被記錄
        user_messages = [h for h in history if h["role"] == "user"]
        assert len(user_messages) == len(messages)
        
        for i, msg in enumerate(messages):
            assert user_messages[i]["content"] == msg
    
    def test_TC_INTE_0023_model_state_consistency(self, chat_model):
        """TC-INTE-0023: 測試模型狀態一致性"""
        # Act
        initial_info = chat_model.get_model_info()
        
        # 執行一些操作
        chat_model.reply("測試")
        chat_model.reply("測試2")
        
        updated_info = chat_model.get_model_info()
        
        # Assert - 模型配置不應改變，只有對話長度改變
        assert initial_info["model_name"] == updated_info["model_name"]
        assert initial_info["temperature"] == updated_info["temperature"]
        assert updated_info["conversation_length"] > initial_info["conversation_length"]
