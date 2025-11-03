"""
BasePage - 所有 Page Object 的基礎類別
提供共用的頁面操作方法
"""

from playwright.sync_api import Page, expect
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """所有頁面對象的基礎類別"""

    def __init__(self, page: Page, base_url: str = "http://localhost:3000"):
        """
        初始化 BasePage

        Args:
            page: Playwright Page 對象
            base_url: 應用程式的基礎 URL
        """
        self.page = page
        self.base_url = base_url

    def navigate_to(self, path: str = ""):
        """
        導航到指定路徑

        Args:
            path: URL 路徑（相對於 base_url）
        """
        url = f"{self.base_url}{path}"
        logger.info(f"導航到: {url}")
        self.page.goto(url)

    def click(self, selector: str, timeout: int = 30000):
        """
        點擊元素

        Args:
            selector: CSS 選擇器
            timeout: 超時時間（毫秒）
        """
        logger.info(f"點擊元素: {selector}")
        self.page.click(selector, timeout=timeout)

    def fill(self, selector: str, text: str, timeout: int = 30000):
        """
        填寫輸入框

        Args:
            selector: CSS 選擇器
            text: 要輸入的文字
            timeout: 超時時間（毫秒）
        """
        logger.info(f"在 {selector} 輸入: {text}")
        self.page.fill(selector, text, timeout=timeout)

    def get_text(self, selector: str, timeout: int = 30000) -> str:
        """
        獲取元素文字內容

        Args:
            selector: CSS 選擇器
            timeout: 超時時間（毫秒）

        Returns:
            元素的文字內容
        """
        logger.info(f"獲取元素文字: {selector}")
        return self.page.text_content(selector, timeout=timeout) or ""

    def wait_for_selector(self, selector: str, timeout: int = 30000):
        """
        等待元素出現

        Args:
            selector: CSS 選擇器
            timeout: 超時時間（毫秒）
        """
        logger.info(f"等待元素: {selector}")
        self.page.wait_for_selector(selector, timeout=timeout)

    def wait_for_url(self, url_pattern: str, timeout: int = 30000):
        """
        等待 URL 變化

        Args:
            url_pattern: URL 模式（支援正則表達式）
            timeout: 超時時間（毫秒）
        """
        logger.info(f"等待 URL 匹配: {url_pattern}")
        self.page.wait_for_url(url_pattern, timeout=timeout)

    def is_visible(self, selector: str) -> bool:
        """
        檢查元素是否可見

        Args:
            selector: CSS 選擇器

        Returns:
            True 如果元素可見，否則 False
        """
        try:
            return self.page.is_visible(selector, timeout=5000)
        except Exception:
            return False

    def screenshot(self, path: str):
        """
        截圖

        Args:
            path: 截圖保存路徑
        """
        logger.info(f"截圖保存至: {path}")
        self.page.screenshot(path=path)

    def get_title(self) -> str:
        """獲取頁面標題"""
        return self.page.title()

    def reload(self):
        """重新載入頁面"""
        logger.info("重新載入頁面")
        self.page.reload()
