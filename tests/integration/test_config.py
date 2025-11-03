"""整合測試範例 - 測試配置載入"""

import pytest
from pathlib import Path


@pytest.mark.integration
def test_TC_INTE_0001_config_loading(config):
    """TC-INTE-0001: 測試配置文件是否正確載入"""
    assert config is not None
    assert "env" in config
    assert config["env"] == "dev"


@pytest.mark.integration
def test_TC_INTE_0002_project_structure(project_root):
    """TC-INTE-0002: 測試專案結構是否正確"""
    # 驗證關鍵目錄存在
    assert (project_root / "tests").exists()
    assert (project_root / "fixtures").exists()
    assert (project_root / "config").exists()

    # 驗證配置文件存在
    assert (project_root / "pytest.ini").exists()
    assert (project_root / "pyproject.toml").exists()
    assert (project_root / "conftest.py").exists()


@pytest.mark.integration
def test_TC_INTE_0003_test_data_directory(test_data_dir):
    """TC-INTE-0003: 測試數據目錄是否可用"""
    assert test_data_dir.exists()
    assert test_data_dir.is_dir()
