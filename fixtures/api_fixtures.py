"""API 測試 Fixtures"""

import pytest


@pytest.fixture
def api_client():
    """API 客戶端 fixture"""
    # TODO: 實作 API 客戶端
    pass


@pytest.fixture
def mock_llm_response():
    """模擬 LLM 回應"""
    return {"response": "您好！我可以幫您查詢帳戶餘額。", "confidence": 0.95, "intent": "account_inquiry"}
