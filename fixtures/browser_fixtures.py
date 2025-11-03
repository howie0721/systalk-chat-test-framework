"""
Browser Fixtures - Playwright 瀏覽器相關 fixtures
提供瀏覽器、頁面等測試資源
"""

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def playwright_instance():
    """
    提供 Playwright 實例（session 級別）
    整個測試會話只啟動一次 Playwright
    """
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright):
    """
    提供瀏覽器實例（session 級別）
    可選：chromium, firefox, webkit
    """
    logger.info("啟動 Chromium 瀏覽器")
    browser = playwright_instance.chromium.launch(
        headless=True,  # 設為 False 可看到瀏覽器視窗
        slow_mo=100,  # 放慢操作速度（毫秒），方便觀察
    )
    yield browser
    logger.info("關閉瀏覽器")
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser):
    """
    提供瀏覽器上下文（function 級別）
    每個測試函數都會獲得全新的上下文
    """
    logger.info("創建新的瀏覽器上下文")
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="zh-TW",
        timezone_id="Asia/Taipei",
    )
    yield context
    logger.info("關閉瀏覽器上下文")
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext, request, reports_dir):
    """
    提供頁面實例（function 級別）
    每個測試函數都會獲得全新的頁面
    測試失敗時自動截圖
    """
    logger.info("創建新頁面")
    page = context.new_page()

    yield page

    # 測試失敗時自動截圖
    if request.node.rep_call.failed:
        screenshot_dir = reports_dir / "screenshots"
        screenshot_dir.mkdir(exist_ok=True)

        screenshot_path = screenshot_dir / f"{request.node.name}_failure.png"
        logger.info(f"測試失敗，保存截圖: {screenshot_path}")
        page.screenshot(path=str(screenshot_path))

    logger.info("關閉頁面")
    page.close()


@pytest.fixture(scope="function")
def mobile_page(browser: Browser, request, reports_dir):
    """
    提供移動裝置模擬頁面（function 級別）
    模擬 iPhone 12 Pro
    """
    logger.info("創建移動裝置模擬上下文")
    iphone_12_pro = {
        "viewport": {"width": 390, "height": 844},
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True,
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15",
    }

    context = browser.new_context(**iphone_12_pro)
    page = context.new_page()

    yield page

    # 測試失敗時自動截圖
    if request.node.rep_call.failed:
        screenshot_dir = reports_dir / "screenshots"
        screenshot_dir.mkdir(exist_ok=True)

        screenshot_path = screenshot_dir / f"{request.node.name}_mobile_failure.png"
        logger.info(f"測試失敗，保存截圖: {screenshot_path}")
        page.screenshot(path=str(screenshot_path))

    page.close()
    context.close()


# Pytest hook 用於獲取測試結果（支援失敗截圖）
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    在測試執行後添加結果到 item，用於失敗截圖
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
