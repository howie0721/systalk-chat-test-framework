"""單元測試範例"""

import pytest


@pytest.mark.smoke
@pytest.mark.unit
def test_TC_UNIT_0001_model_reply_hello(chat_model):
    """TC-UNIT-0001: 驗證 AI 模型能正確回應「你好」"""
    # Arrange（準備）
    prompt = "你好"

    # Act（執行）
    response = chat_model.reply(prompt)

    # Assert（驗證）
    assert "你好" in response or "Hello" in response, "模型回應應包含問候語"


@pytest.mark.smoke
@pytest.mark.unit
def test_TC_UNIT_0002_fixture_usage(sample_chat_message):
    """TC-UNIT-0002: 測試 fixture 的使用"""
    # 使用 conftest.py 中定義的 fixture
    assert "user_id" in sample_chat_message
    assert "message" in sample_chat_message
    assert sample_chat_message["user_id"] == "test_user_001"


@pytest.mark.unit
def test_TC_UNIT_0003_string_operations():
    """TC-UNIT-0003: 測試字串操作"""
    text = "Hello SysTalk.Chat"

    assert "SysTalk" in text
    assert text.startswith("Hello")
    assert len(text) > 0
