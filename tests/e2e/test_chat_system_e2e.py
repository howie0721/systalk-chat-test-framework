"""
AI 聊天系統 E2E 測試
測試完整的使用者互動流程
"""

import pytest
import time


@pytest.mark.e2e
class TestChatSystemE2E:
    """聊天系統端到端測試"""
    
    def test_TC_E2E_0011_complete_user_journey(self, chat_model):
        """TC-E2E-0011: 測試完整的使用者旅程"""
        # Scenario: 用戶從打招呼到完成查詢的完整流程
        
        # Step 1: 用戶打招呼
        greeting_response = chat_model.reply("你好")
        assert "你好" in greeting_response or "Hello" in greeting_response
        
        # Step 2: 用戶詢問功能
        capability_response = chat_model.reply("你能幫我做什麼？")
        assert len(capability_response) > 0
        
        # Step 3: 用戶進行帳戶查詢
        query_response = chat_model.reply("我想查詢我的帳戶餘額")
        assert "帳戶" in query_response or "餘額" in query_response
        
        # Step 4: 用戶道謝並結束
        farewell_response = chat_model.reply("謝謝你的幫助")
        assert len(farewell_response) > 0
        
        # Verify: 整個對話歷史應該被完整記錄
        history = chat_model.get_conversation_history()
        assert len(history) == 8  # 4 user + 4 assistant messages
    
    def test_TC_E2E_0012_banking_inquiry_flow(self, chat_model):
        """TC-E2E-0012: 測試銀行業務查詢流程"""
        # Scenario: 用戶查詢銀行服務的完整流程
        
        # Step 1: 初始詢問
        response1 = chat_model.reply("我想了解你們的服務")
        assert response1 is not None
        
        # Step 2: 具體查詢
        response2 = chat_model.reply("帳戶餘額是多少？")
        assert "餘額" in response2 or "帳戶" in response2
        
        # Step 3: 後續問題
        response3 = chat_model.reply("有其他收費嗎？")
        assert len(response3) > 0
        
        # Verify: 對話流程完整
        history = chat_model.get_conversation_history()
        assert len(history) == 6
    
    def test_TC_E2E_0013_multi_topic_conversation(self, chat_model):
        """TC-E2E-0013: 測試多主題對話流程"""
        # Scenario: 用戶在同一會話中討論多個主題
        
        topics_and_responses = [
            ("今天天氣如何？", ["天氣", "溫度", "晴", "雨", "台北"]),
            ("我的帳戶餘額是多少？", ["帳戶", "餘額"]),
            ("你好嗎？", ["好", "很好", "您"]),
        ]
        
        for prompt, expected_keywords in topics_and_responses:
            response = chat_model.reply(prompt)
            # 至少包含一個預期關鍵字
            assert any(kw in response for kw in expected_keywords), \
                f"回應應包含 {expected_keywords} 之一，但得到：{response}"


@pytest.mark.e2e
class TestChatSystemErrorHandling:
    """聊天系統錯誤處理 E2E 測試"""
    
    def test_TC_E2E_0014_graceful_error_recovery(self, chat_model):
        """TC-E2E-0014: 測試優雅的錯誤恢復"""
        # Scenario: 用戶輸入錯誤後能正常繼續對話
        
        # Step 1: 正常對話
        response1 = chat_model.reply("你好")
        assert len(response1) > 0
        
        # Step 2: 發送空輸入（錯誤）
        error_response = chat_model.reply("")
        assert error_response == "請輸入有效的內容"
        
        # Step 3: 發送純空白（錯誤）
        whitespace_response = chat_model.reply("   ")
        assert whitespace_response == "請輸入有效的內容"
        
        # Step 4: 恢復正常對話
        recovery_response = chat_model.reply("現在我有一個正常的問題")
        assert recovery_response != "請輸入有效的內容"
        assert len(recovery_response) > 0
        
        # Verify: 系統應該記錄所有有效互動（空輸入不會被記錄）
        history = chat_model.get_conversation_history()
        assert len(history) == 4  # 2 次有效對話 (第一個 "你好" 和最後的恢復對話)
    
    def test_TC_E2E_0015_invalid_input_sequence(self, chat_model):
        """TC-E2E-0015: 測試連續無效輸入的處理"""
        # Scenario: 用戶連續發送無效輸入
        
        invalid_inputs = ["", "   ", "\n\n", "\t\t"]
        
        for invalid_input in invalid_inputs:
            response = chat_model.reply(invalid_input)
            assert response == "請輸入有效的內容"
        
        # 最後發送有效輸入
        valid_response = chat_model.reply("這是一個有效問題")
        assert valid_response != "請輸入有效的內容"


@pytest.mark.e2e
@pytest.mark.smoke
class TestChatSystemBasicFunctionality:
    """聊天系統基本功能 E2E 測試"""
    
    def test_TC_E2E_0016_quick_smoke_test(self, chat_model):
        """TC-E2E-0016: 快速煙霧測試（驗證系統基本可用）"""
        # Arrange
        test_prompt = "你好，測試一下"
        
        # Act
        response = chat_model.reply(test_prompt)
        
        # Assert
        assert response is not None
        assert len(response) > 0
        assert response != "請輸入有效的內容"
        assert chat_model.is_initialized()
    
    def test_TC_E2E_0017_session_management(self, chat_model):
        """TC-E2E-0017: 測試會話管理功能"""
        # Scenario: 驗證會話的生命週期管理
        
        # Step 1: 開始新會話
        chat_model.reply("開始會話")
        initial_length = len(chat_model.get_conversation_history())
        assert initial_length > 0
        
        # Step 2: 繼續會話
        chat_model.reply("繼續對話")
        continued_length = len(chat_model.get_conversation_history())
        assert continued_length > initial_length
        
        # Step 3: 結束會話（清除）
        chat_model.clear_history()
        final_length = len(chat_model.get_conversation_history())
        assert final_length == 0
        
        # Step 4: 開始新會話
        chat_model.reply("新的會話")
        new_length = len(chat_model.get_conversation_history())
        assert new_length == 2


@pytest.mark.e2e
class TestChatSystemRealisticScenarios:
    """聊天系統真實場景 E2E 測試"""
    
    def test_TC_E2E_0018_customer_support_scenario(self, chat_model):
        """TC-E2E-0018: 測試客戶支援場景"""
        # Scenario: 完整的客戶支援對話
        
        conversation = [
            {
                "user": "你好，我需要幫助",
                "verify": lambda r: len(r) > 0 and ("你好" in r or "幫助" in r)
            },
            {
                "user": "我的帳戶有問題",
                "verify": lambda r: "帳戶" in r
            },
            {
                "user": "我想查詢餘額",
                "verify": lambda r: "餘額" in r or "帳戶" in r
            },
            {
                "user": "謝謝你的協助",
                "verify": lambda r: len(r) > 0
            }
        ]
        
        for turn in conversation:
            response = chat_model.reply(turn["user"])
            assert turn["verify"](response), f"回應驗證失敗：{response}"
    
    def test_TC_E2E_0019_information_gathering_flow(self, chat_model):
        """TC-E2E-0019: 測試資訊收集流程"""
        # Scenario: AI 從用戶收集資訊的流程
        
        # 用戶提供不完整資訊
        response1 = chat_model.reply("我想辦理業務")
        assert len(response1) > 0
        
        # 用戶提供更多細節
        response2 = chat_model.reply("我想辦理信用卡")
        assert len(response2) > 0
        
        # 用戶確認
        response3 = chat_model.reply("是的，請幫我辦理")
        assert len(response3) > 0
        
        # Verify: 完整的對話流程
        history = chat_model.get_conversation_history()
        assert len(history) == 6  # 3 user + 3 assistant
    
    def test_TC_E2E_0020_context_aware_conversation(self, chat_model):
        """TC-E2E-0020: 測試上下文感知對話"""
        # Scenario: AI 能夠根據對話上下文回應
        
        # 建立上下文
        chat_model.reply("我叫李四")
        
        # 後續對話應該能記住用戶名稱（在實際 LLM 中）
        # 這裡主要驗證對話歷史被正確記錄
        history = chat_model.get_conversation_history()
        assert any("李四" in msg["content"] for msg in history if msg["role"] == "user")


@pytest.mark.e2e
@pytest.mark.performance
class TestChatSystemPerformanceE2E:
    """聊天系統效能 E2E 測試"""
    
    def test_TC_E2E_0021_response_time_under_load(self, chat_model):
        """TC-E2E-0021: 測試負載下的響應時間"""
        # Scenario: 多次請求的響應時間應該穩定
        
        response_times = []
        num_requests = 20
        
        for i in range(num_requests):
            start = time.time()
            response = chat_model.reply(f"測試問題 {i}")
            end = time.time()
            
            response_times.append(end - start)
            assert response is not None
        
        # 計算平均響應時間
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        
        # Assert
        assert avg_time < 0.5  # 平均響應時間應小於 0.5 秒
        assert max_time < 1.0  # 最大響應時間應小於 1 秒
    
    def test_TC_E2E_0022_sustained_conversation_performance(self, chat_model):
        """TC-E2E-0022: 測試持續對話的效能"""
        # Scenario: 長時間對話不應導致效能下降
        
        num_turns = 30
        start_time = time.time()
        
        for i in range(num_turns):
            response = chat_model.reply(f"對話輪次 {i}")
            assert response is not None
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time_per_turn = total_time / num_turns
        
        # Assert
        assert total_time < 30  # 30 輪對話應在 30 秒內完成
        assert avg_time_per_turn < 1.0


@pytest.mark.e2e
class TestChatSystemIntegrationPoints:
    """聊天系統整合點 E2E 測試"""
    
    def test_TC_E2E_0023_model_initialization_in_workflow(self):
        """TC-E2E-0023: 測試工作流程中的模型初始化"""
        from ai_models.chat_model import ChatModel
        
        # Scenario: 模擬完整的模型生命週期
        
        # Step 1: 初始化
        model = ChatModel(model_name="gpt-3.5-turbo", temperature=0.7)
        assert model.is_initialized()
        
        # Step 2: 使用
        response = model.reply("測試")
        assert response is not None
        
        # Step 3: 檢查狀態
        info = model.get_model_info()
        assert info["conversation_length"] > 0
        
        # Step 4: 清理
        model.clear_history()
        assert len(model.get_conversation_history()) == 0
    
    def test_TC_E2E_0024_multiple_models_interaction(self):
        """TC-E2E-0024: 測試多個模型實例的交互"""
        from ai_models.chat_model import ChatModel
        
        # Scenario: 同時使用多個模型實例
        
        model1 = ChatModel(temperature=0.1)
        model2 = ChatModel(temperature=0.9)
        
        prompt = "這是測試"
        
        response1 = model1.reply(prompt)
        response2 = model2.reply(prompt)
        
        # 兩個模型應該獨立運作
        assert response1 is not None
        assert response2 is not None
        
        # 對話歷史應該分開
        history1 = model1.get_conversation_history()
        history2 = model2.get_conversation_history()
        
        assert len(history1) == 2
        assert len(history2) == 2
        
        # Cleanup
        model1.clear_history()
        model2.clear_history()
    
    def test_TC_E2E_0025_end_to_end_with_validation(self, chat_model):
        """TC-E2E-0025: 端到端測試包含輸入驗證"""
        # Scenario: 完整流程包含輸入驗證
        
        test_inputs = [
            ("有效輸入", True),
            ("", False),
            ("   ", False),
            ("這是另一個有效輸入", True),
        ]
        
        for input_text, should_be_valid in test_inputs:
            # 驗證輸入
            is_valid = chat_model.validate_input(input_text)
            assert is_valid == should_be_valid
            
            # 發送請求
            response = chat_model.reply(input_text)
            
            if should_be_valid:
                assert response != "請輸入有效的內容"
            else:
                assert response == "請輸入有效的內容"
