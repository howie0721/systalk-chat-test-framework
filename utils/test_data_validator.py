"""
測試資料驗證器
驗證測試資料的完整性和正確性
"""
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class TestDataValidator:
    """測試資料驗證器"""

    def __init__(self):
        self.validation_errors = []

    def validate_chat_messages(self, data: List[Dict[str, Any]]) -> bool:
        """
        驗證聊天訊息資料

        Args:
            data: 聊天訊息資料列表

        Returns:
            驗證是否通過
        """
        required_fields = ["message_id", "user_id", "message", "intent", "timestamp"]

        for i, item in enumerate(data):
            # 檢查必要欄位
            for field in required_fields:
                if field not in item:
                    self.validation_errors.append(f"Item {i}: Missing required field '{field}'")

            # 檢查資料型別
            if "message_id" in item and not isinstance(item["message_id"], str):
                self.validation_errors.append(f"Item {i}: 'message_id' must be string")

            if "message" in item and not isinstance(item["message"], str):
                self.validation_errors.append(f"Item {i}: 'message' must be string")

            if "message" in item and len(item["message"]) == 0:
                self.validation_errors.append(f"Item {i}: 'message' cannot be empty")

        return len(self.validation_errors) == 0

    def validate_ai_test_cases(self, data: List[Dict[str, Any]]) -> bool:
        """
        驗證 AI 測試案例

        Args:
            data: AI 測試案例列表

        Returns:
            驗證是否通過
        """
        required_fields = ["test_id", "category", "question", "expected_answer"]
        valid_categories = ["factual", "calculation", "reasoning", "contextual"]

        for i, item in enumerate(data):
            # 檢查必要欄位
            for field in required_fields:
                if field not in item:
                    self.validation_errors.append(f"Item {i}: Missing required field '{field}'")

            # 檢查類別
            if "category" in item and item["category"] not in valid_categories:
                self.validation_errors.append(
                    f"Item {i}: Invalid category '{item['category']}'. " f"Must be one of {valid_categories}"
                )

            # 檢查問題和答案不為空
            if "question" in item and len(item["question"]) == 0:
                self.validation_errors.append(f"Item {i}: 'question' cannot be empty")

            if "expected_answer" in item and len(item["expected_answer"]) == 0:
                self.validation_errors.append(f"Item {i}: 'expected_answer' cannot be empty")

        return len(self.validation_errors) == 0

    def validate_prompt_injection_cases(self, data: List[Dict[str, Any]]) -> bool:
        """
        驗證提示注入測試案例

        Args:
            data: 提示注入測試案例列表

        Returns:
            驗證是否通過
        """
        required_fields = ["test_id", "type", "prompt", "risk_level"]
        valid_risk_levels = ["low", "medium", "high", "critical"]

        for i, item in enumerate(data):
            # 檢查必要欄位
            for field in required_fields:
                if field not in item:
                    self.validation_errors.append(f"Item {i}: Missing required field '{field}'")

            # 檢查風險等級
            if "risk_level" in item and item["risk_level"] not in valid_risk_levels:
                self.validation_errors.append(
                    f"Item {i}: Invalid risk_level '{item['risk_level']}'. "
                    f"Must be one of {valid_risk_levels}"
                )

            # 檢查提示不為空
            if "prompt" in item and len(item["prompt"]) == 0:
                self.validation_errors.append(f"Item {i}: 'prompt' cannot be empty")

        return len(self.validation_errors) == 0

    def validate_bias_test_cases(self, data: List[Dict[str, Any]]) -> bool:
        """
        驗證偏見測試案例

        Args:
            data: 偏見測試案例列表

        Returns:
            驗證是否通過
        """
        required_fields = ["test_id", "category", "question"]
        valid_categories = ["gender", "age", "race", "occupation"]

        for i, item in enumerate(data):
            # 檢查必要欄位
            for field in required_fields:
                if field not in item:
                    self.validation_errors.append(f"Item {i}: Missing required field '{field}'")

            # 檢查類別
            if "category" in item and item["category"] not in valid_categories:
                self.validation_errors.append(
                    f"Item {i}: Invalid category '{item['category']}'. " f"Must be one of {valid_categories}"
                )

        return len(self.validation_errors) == 0

    def validate_performance_test_data(self, data: List[Dict[str, Any]]) -> bool:
        """
        驗證效能測試資料

        Args:
            data: 效能測試資料列表

        Returns:
            驗證是否通過
        """
        required_fields = ["test_id", "input_text", "input_length"]

        for i, item in enumerate(data):
            # 檢查必要欄位
            for field in required_fields:
                if field not in item:
                    self.validation_errors.append(f"Item {i}: Missing required field '{field}'")

            # 檢查輸入長度與實際文字長度是否一致
            if "input_text" in item and "input_length" in item:
                actual_length = len(item["input_text"])
                declared_length = item["input_length"]
                if actual_length != declared_length:
                    self.validation_errors.append(
                        f"Item {i}: input_length mismatch. "
                        f"Declared: {declared_length}, Actual: {actual_length}"
                    )

        return len(self.validation_errors) == 0

    def validate_file(self, filepath: Path, data_type: str) -> bool:
        """
        驗證檔案

        Args:
            filepath: 檔案路徑
            data_type: 資料類型 (chat_messages, ai_test_cases, etc.)

        Returns:
            驗證是否通過
        """
        self.validation_errors = []

        try:
            # 讀取檔案
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 檢查資料是否為列表
            if not isinstance(data, list):
                self.validation_errors.append("Data must be a list")
                return False

            # 檢查是否為空
            if len(data) == 0:
                self.validation_errors.append("Data list is empty")
                return False

            # 根據資料類型進行驗證
            validators = {
                "chat_messages": self.validate_chat_messages,
                "ai_test_cases": self.validate_ai_test_cases,
                "prompt_injection_cases": self.validate_prompt_injection_cases,
                "bias_test_cases": self.validate_bias_test_cases,
                "performance_test_data": self.validate_performance_test_data,
            }

            if data_type not in validators:
                self.validation_errors.append(f"Unknown data type: {data_type}")
                return False

            # 執行驗證
            result = validators[data_type](data)

            if result:
                logger.info(f"✅ {filepath.name} 驗證通過 ({len(data)} 筆資料)")
            else:
                logger.error(f"❌ {filepath.name} 驗證失敗")
                for error in self.validation_errors:
                    logger.error(f"  - {error}")

            return result

        except json.JSONDecodeError as e:
            self.validation_errors.append(f"Invalid JSON format: {e}")
            logger.error(f"❌ {filepath.name} JSON 格式錯誤: {e}")
            return False
        except Exception as e:
            self.validation_errors.append(f"Validation error: {e}")
            logger.error(f"❌ {filepath.name} 驗證錯誤: {e}")
            return False

    def validate_all_datasets(self, data_dir: Path) -> bool:
        """
        驗證所有資料集

        Args:
            data_dir: 資料目錄

        Returns:
            所有驗證是否通過
        """
        print("\n📋 開始驗證測試資料集...")

        datasets = {
            "chat_messages.json": "chat_messages",
            "ai_test_cases.json": "ai_test_cases",
            "prompt_injection_cases.json": "prompt_injection_cases",
            "bias_test_cases.json": "bias_test_cases",
            "performance_test_data.json": "performance_test_data",
        }

        all_valid = True
        for filename, data_type in datasets.items():
            filepath = data_dir / filename
            if filepath.exists():
                if not self.validate_file(filepath, data_type):
                    all_valid = False
            else:
                print(f"⚠️  檔案不存在: {filename}")
                all_valid = False

        if all_valid:
            print("\n✅ 所有資料集驗證通過！")
        else:
            print("\n❌ 部分資料集驗證失敗")

        return all_valid


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    validator = TestDataValidator()
    data_path = Path(__file__).parent.parent / "data" / "test_datasets"
    validator.validate_all_datasets(data_path)
