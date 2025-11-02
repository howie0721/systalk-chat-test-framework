"""
全局 Pytest Fixtures 配置
提供測試所需的共用 fixtures
"""
import pytest
from pathlib import Path


# ==================== 路徑 Fixtures ====================

@pytest.fixture(scope="session")
def project_root():
    """專案根目錄"""
    return Path(__file__).parent


@pytest.fixture(scope="session")
def test_data_dir(project_root):
    """測試數據目錄"""
    return project_root / "data" / "test_datasets"


@pytest.fixture(scope="session")
def golden_data_dir(project_root):
    """黃金數據集目錄"""
    return project_root / "data" / "golden_datasets"


@pytest.fixture(scope="session")
def reports_dir(project_root):
    """報告輸出目錄"""
    reports_path = project_root / "reports"
    reports_path.mkdir(exist_ok=True)
    return reports_path


# ==================== 環境配置 Fixtures ====================

@pytest.fixture(scope="session")
def test_env():
    """測試環境配置"""
    import os
    return os.getenv("TEST_ENV", "dev")


@pytest.fixture(scope="session")
def config(test_env, project_root):
    """載入配置文件"""
    import yaml
    config_file = project_root / "config" / "environments" / f"{test_env}.yaml"
    
    # 如果配置文件不存在，返回預設配置
    if not config_file.exists():
        return {
            "env": test_env,
            "base_url": "http://localhost:3000",
            "api_timeout": 30
        }
    
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


# ==================== 測試數據 Fixtures ====================

@pytest.fixture
def sample_chat_message():
    """範例聊天訊息"""
    return {
        "user_id": "test_user_001",
        "message": "你好，我想查詢帳戶餘額",
        "timestamp": "2025-11-02T10:00:00Z"
    }


@pytest.fixture
def sample_test_cases():
    """範例測試案例集"""
    return [
        {"input": "查詢餘額", "expected_intent": "account_inquiry"},
        {"input": "申請信用卡", "expected_intent": "product_inquiry"},
        {"input": "投訴服務", "expected_intent": "complaint"},
    ]


# ==================== Pytest Hooks ====================

def pytest_configure(config):
    """Pytest 啟動時執行"""
    print("\n🚀 開始執行測試...")
    print(f"📁 專案目錄: {Path.cwd()}")
    print(f"🧪 測試環境: {config.getoption('--env', default='dev')}")


def pytest_collection_modifyitems(config, items):
    """自動為測試添加標記"""
    for item in items:
        # 根據路徑自動添加標記
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
        elif "ai_quality" in str(item.fspath):
            item.add_marker(pytest.mark.ai_quality)
        elif "ai_specific" in str(item.fspath):
            item.add_marker(pytest.mark.ai_specific)
        elif "llm_specific" in str(item.fspath):
            item.add_marker(pytest.mark.llm_specific)
        elif "security" in str(item.fspath):
            item.add_marker(pytest.mark.security)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """測試完成後顯示摘要"""
    print("\n" + "="*60)
    print("📊 測試執行摘要")
    print("="*60)