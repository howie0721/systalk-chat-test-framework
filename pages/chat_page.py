"""
ChatPage - SysTalk.Chat 聊天頁面 Page Object
封裝聊天介面的元素和操作
"""

from pages.base_page import BasePage
from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)


class ChatPage(BasePage):
    """SysTalk.Chat 聊天頁面 Page Object"""

    # 頁面元素定位器（Locators）
    MESSAGE_INPUT = "#message-input"
    SEND_BUTTON = "#send-button"
    CHAT_MESSAGES = ".chat-message"
    USER_MESSAGE = ".user-message"
    AI_RESPONSE = ".ai-response"
    LOADING_INDICATOR = ".loading-indicator"
    ERROR_MESSAGE = ".error-message"

    def __init__(self, page: Page, base_url: str = "http://localhost:3000"):
        """初始化 ChatPage"""
        super().__init__(page, base_url)

    def open(self):
        """打開聊天頁面"""
        self.navigate_to("/chat")
        self.wait_for_page_load()
        return self

    def wait_for_page_load(self):
        """等待頁面載入完成"""
        logger.info("等待聊天頁面載入")
        self.wait_for_selector(self.MESSAGE_INPUT, timeout=10000)

    def send_message(self, message: str):
        """
        發送聊天訊息

        Args:
            message: 要發送的訊息內容
        """
        logger.info(f"發送訊息: {message}")
        self.fill(self.MESSAGE_INPUT, message)
        self.click(self.SEND_BUTTON)
        # 等待訊息發送完成（loading indicator 消失）
        self.wait_for_loading_complete()
        return self

    def get_last_user_message(self) -> str:
        """
        獲取最後一條用戶訊息

        Returns:
            最後一條用戶訊息的文字內容
        """
        logger.info("獲取最後一條用戶訊息")
        messages = self.page.query_selector_all(self.USER_MESSAGE)
        if messages:
            return messages[-1].text_content() or ""
        return ""

    def get_last_ai_response(self) -> str:
        """
        獲取最後一條 AI 回應

        Returns:
            最後一條 AI 回應的文字內容
        """
        logger.info("獲取最後一條 AI 回應")
        # 等待 AI 回應出現
        self.wait_for_selector(self.AI_RESPONSE, timeout=30000)
        responses = self.page.query_selector_all(self.AI_RESPONSE)
        if responses:
            return responses[-1].text_content() or ""
        return ""

    def get_all_messages(self) -> list[str]:
        """
        獲取所有聊天訊息

        Returns:
            所有訊息的列表
        """
        logger.info("獲取所有聊天訊息")
        messages = self.page.query_selector_all(self.CHAT_MESSAGES)
        return [msg.text_content() or "" for msg in messages]

    def wait_for_loading_complete(self, timeout: int = 30000):
        """
        等待載入完成（loading indicator 消失）

        Args:
            timeout: 超時時間（毫秒）
        """
        try:
            # 如果 loading indicator 存在，等待它消失
            if self.is_visible(self.LOADING_INDICATOR):
                logger.info("等待載入完成")
                self.page.wait_for_selector(self.LOADING_INDICATOR, state="hidden", timeout=timeout)
        except Exception as e:
            logger.warning(f"等待載入時發生異常（可能本來就不存在）: {e}")

    def is_error_displayed(self) -> bool:
        """
        檢查是否顯示錯誤訊息

        Returns:
            True 如果有錯誤訊息顯示
        """
        return self.is_visible(self.ERROR_MESSAGE)

    def get_error_message(self) -> str:
        """
        獲取錯誤訊息內容

        Returns:
            錯誤訊息文字
        """
        if self.is_error_displayed():
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def clear_chat(self):
        """清空聊天記錄（如果有清空按鈕）"""
        clear_button = "#clear-chat"
        if self.is_visible(clear_button):
            logger.info("清空聊天記錄")
            self.click(clear_button)
        return self

    def is_send_button_enabled(self) -> bool:
        """
        檢查發送按鈕是否啟用

        Returns:
            True 如果發送按鈕啟用
        """
        return not self.page.is_disabled(self.SEND_BUTTON)
