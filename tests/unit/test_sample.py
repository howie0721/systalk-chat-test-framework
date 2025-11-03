"""單元測試範例"""

import pytest


@pytest.mark.smoke
@pytest.mark.unit
def test_basic_assertion():
    """TC-UNIT-0001: 最基礎的測試：驗證 Python 基本運算"""
    # Arrange（準備）
    a = 1
    b = 2

    # Act（執行）
    result = a + b

    # Assert（驗證）
    assert result == 3, "1 + 2 應該等於 3"


@pytest.mark.smoke
@pytest.mark.unit
def test_fixture_usage(sample_chat_message):
    """TC-UNIT-0002: 測試 fixture 的使用"""
    # 使用 conftest.py 中定義的 fixture
    assert "user_id" in sample_chat_message
    assert "message" in sample_chat_message
    assert sample_chat_message["user_id"] == "test_user_001"


@pytest.mark.unit
def test_string_operations():
    """TC-UNIT-0003: 測試字串操作"""
    text = "Hello SysTalk.Chat"

    assert "SysTalk" in text
    assert text.startswith("Hello")
    assert len(text) > 0
