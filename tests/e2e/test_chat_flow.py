"""
E2E 測試 - 聊天流程測試
使用 Page Object Model 測試完整的聊天互動流程
"""

import pytest
from pages.chat_page import ChatPage


@pytest.mark.e2e
@pytest.mark.skip(reason="需要實際運行的 SysTalk.Chat 應用程式")
def test_TC_E2E_0001_send_message_and_get_response(page):
    """
    TC-E2E-0001: 測試發送訊息並接收 AI 回應

    測試流程：
    1. 打開聊天頁面
    2. 發送用戶訊息
    3. 等待 AI 回應
    4. 驗證回應內容
    """
    # Arrange（準備）
    chat_page = ChatPage(page)
    chat_page.open()
    user_message = "你好，我想查詢帳戶餘額"

    # Act（執行）
    chat_page.send_message(user_message)

    # Assert（驗證）
    last_user_msg = chat_page.get_last_user_message()
    assert user_message in last_user_msg, "用戶訊息應該顯示在聊天記錄中"

    ai_response = chat_page.get_last_ai_response()
    assert ai_response, "AI 應該回應用戶訊息"
    assert len(ai_response) > 0, "AI 回應不應為空"


@pytest.mark.e2e
@pytest.mark.skip(reason="需要實際運行的 SysTalk.Chat 應用程式")
def test_TC_E2E_0002_multiple_messages_conversation(page):
    """
    TC-E2E-0002: 測試多輪對話

    測試流程：
    1. 打開聊天頁面
    2. 發送第一條訊息
    3. 獲取回應
    4. 發送第二條訊息（基於第一條的回應）
    5. 驗證對話連貫性
    """
    # Arrange
    chat_page = ChatPage(page)
    chat_page.open()

    # Act - 第一輪對話
    first_message = "你好"
    chat_page.send_message(first_message)
    first_response = chat_page.get_last_ai_response()

    # Act - 第二輪對話
    second_message = "我想知道你能幫我做什麼"
    chat_page.send_message(second_message)
    second_response = chat_page.get_last_ai_response()

    # Assert
    all_messages = chat_page.get_all_messages()
    assert len(all_messages) >= 4, "應該至少有 4 條訊息（2 條用戶 + 2 條 AI）"
    assert first_response, "第一條 AI 回應不應為空"
    assert second_response, "第二條 AI 回應不應為空"
    assert first_response != second_response, "兩次回應應該不同"


@pytest.mark.e2e
@pytest.mark.skip(reason="需要實際運行的 SysTalk.Chat 應用程式")
def test_TC_E2E_0003_empty_message_validation(page):
    """
    TC-E2E-0003: 測試空訊息驗證

    測試流程：
    1. 打開聊天頁面
    2. 嘗試發送空訊息
    3. 驗證無法發送或顯示錯誤
    """
    # Arrange
    chat_page = ChatPage(page)
    chat_page.open()

    # Act
    messages_before = len(chat_page.get_all_messages())

    # 嘗試發送空訊息
    chat_page.fill(ChatPage.MESSAGE_INPUT, "")

    # Assert
    # 發送按鈕應該被禁用，或者訊息數量沒有增加
    is_button_enabled = chat_page.is_send_button_enabled()

    if is_button_enabled:
        # 如果按鈕可點，發送後應該沒有新訊息
        chat_page.click(ChatPage.SEND_BUTTON)
        messages_after = len(chat_page.get_all_messages())
        assert messages_after == messages_before, "空訊息不應該被發送"
    else:
        # 按鈕應該被禁用
        assert not is_button_enabled, "空訊息時發送按鈕應該被禁用"


@pytest.mark.e2e
@pytest.mark.skip(reason="需要實際運行的 SysTalk.Chat 應用程式")
def test_TC_E2E_0004_page_reload_preserves_chat(page):
    """
    TC-E2E-0004: 測試頁面重新載入後聊天記錄保存

    測試流程：
    1. 打開聊天頁面
    2. 發送訊息
    3. 重新載入頁面
    4. 驗證聊天記錄是否保存
    """
    # Arrange
    chat_page = ChatPage(page)
    chat_page.open()

    # Act - 發送訊息
    test_message = "這是測試訊息"
    chat_page.send_message(test_message)
    messages_before = len(chat_page.get_all_messages())

    # Act - 重新載入頁面
    chat_page.reload()
    chat_page.wait_for_page_load()

    # Assert
    messages_after = len(chat_page.get_all_messages())
    # 根據實際應用行為，決定是否應該保留訊息
    # 這裡假設訊息應該被保留
    assert messages_after >= messages_before, "重新載入後聊天記錄應該被保留"


@pytest.mark.e2e
@pytest.mark.smoke
def test_TC_E2E_0005_chat_page_mock_demo(page):
    """
    TC-E2E-0005: 聊天頁面 Mock 示範測試（不需要實際應用）
    展示 POM 的使用方式和測試結構

    這個測試用於：
    1. 驗證 POM 架構正確
    2. 展示測試撰寫方式
    3. CI/CD 中可以執行（不依賴實際應用）
    """
    # Arrange
    chat_page = ChatPage(page)

    # 這裡僅展示 POM 的結構和方法
    # 實際測試需要真實的應用程式

    # Assert - 驗證 Page Object 方法存在
    assert hasattr(chat_page, "open"), "ChatPage 應該有 open 方法"
    assert hasattr(chat_page, "send_message"), "ChatPage 應該有 send_message 方法"
    assert hasattr(chat_page, "get_last_ai_response"), "ChatPage 應該有 get_last_ai_response 方法"
    assert hasattr(chat_page, "get_all_messages"), "ChatPage 應該有 get_all_messages 方法"

    # 驗證 locators 定義
    assert ChatPage.MESSAGE_INPUT, "應該定義 MESSAGE_INPUT locator"
    assert ChatPage.SEND_BUTTON, "應該定義 SEND_BUTTON locator"
    assert ChatPage.AI_RESPONSE, "應該定義 AI_RESPONSE locator"

    print("✅ Page Object Model 架構驗證通過")
