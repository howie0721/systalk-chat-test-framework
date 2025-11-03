# 測試框架使用指南

## 目錄

- [快速開始](#快速開始)
- [測試類型](#測試類型)
- [編寫測試](#編寫測試)
- [執行測試](#執行測試)
- [測試報告](#測試報告)
- [最佳實踐](#最佳實踐)
- [常見問題](#常見問題)

## 快速開始

### 安裝依賴

```bash
# 克隆專案
git clone <repository-url>
cd systalk-chat-test-framework

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt

# 安裝 Playwright 瀏覽器
playwright install chromium
```

### 執行第一個測試

```bash
# 執行所有測試
pytest

# 執行單元測試
pytest tests/unit/ -v

# 執行特定測試檔案
pytest tests/unit/test_sample.py -v
```

## 測試類型

本框架支援多種測試類型：

### 1. 單元測試 (Unit Tests)

測試單個函數或類別的功能。

```python
# tests/unit/test_utils.py
def test_string_formatting():
    from utils.helpers import format_message
    result = format_message("Hello", "World")
    assert result == "Hello, World"
```

### 2. 整合測試 (Integration Tests)

測試多個元件之間的互動。

```python
# tests/integration/test_config.py
def test_config_loading():
    from utils.config_loader import load_config
    config = load_config("dev")
    assert config["env"] == "dev"
    assert "base_url" in config
```

### 3. E2E 測試 (End-to-End Tests)

測試完整的使用者流程。

```python
# tests/e2e/test_chat_flow.py
@pytest.mark.e2e
def test_complete_chat_flow(page):
    from pages.chat_page import ChatPage
    
    chat_page = ChatPage(page)
    chat_page.navigate()
    chat_page.send_message("你好")
    response = chat_page.get_last_response()
    assert response is not None
```

### 4. AI 品質測試 (AI Quality Tests)

測試 AI 模型的輸出品質。

```python
# tests/ai_quality/test_response_quality.py
def test_response_coherence():
    from ai_models.response_evaluator import ResponseEvaluator
    
    evaluator = ResponseEvaluator()
    result = evaluator.evaluate_coherence(
        "什麼是機器學習？",
        "機器學習是人工智慧的一個分支..."
    )
    assert result["score"] >= 0.7
```

### 5. 安全測試 (Security Tests)

測試系統的安全性。

```python
# tests/llm_specific/test_prompt_injection.py
def test_prompt_injection_defense():
    from ai_models.security_tester import SecurityTester
    
    tester = SecurityTester()
    result = tester.test_injection("忽略之前的指令...")
    assert result["is_safe"] == True
```

## 編寫測試

### 基本測試結構

```python
import pytest

# Fixture 定義
@pytest.fixture
def sample_data():
    return {"key": "value"}

# 測試函數
def test_example(sample_data):
    """測試說明"""
    # Arrange (準備)
    expected = "value"
    
    # Act (執行)
    actual = sample_data["key"]
    
    # Assert (驗證)
    assert actual == expected
```

### 使用 Fixtures

```python
# tests/conftest.py 中定義的全域 fixtures

def test_with_project_root(project_root):
    """使用專案根目錄"""
    assert project_root.exists()

def test_with_config(config):
    """使用配置"""
    assert config["env"] in ["dev", "staging", "prod"]

def test_with_test_data(test_data_dir):
    """使用測試資料"""
    data_file = test_data_dir / "chat_messages.json"
    assert data_file.exists()
```

### 使用標記 (Markers)

```python
import pytest

@pytest.mark.unit
def test_unit_example():
    """單元測試"""
    pass

@pytest.mark.integration
def test_integration_example():
    """整合測試"""
    pass

@pytest.mark.slow
def test_slow_example():
    """慢速測試"""
    pass

@pytest.mark.skipif(condition, reason="...")
def test_conditional():
    """條件跳過"""
    pass

@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_parametrized(input, expected):
    """參數化測試"""
    assert input * 2 == expected
```

### AI 測試編寫

#### 回應品質測試

```python
def test_response_quality():
    from ai_models.response_evaluator import ResponseEvaluator
    
    evaluator = ResponseEvaluator()
    result = evaluator.evaluate(
        question="什麼是人工智慧？",
        response="人工智慧是計算機科學的一個分支，致力於創建能夠執行通常需要人類智慧的任務的系統。"
    )
    
    assert result["coherence"] >= 0.7
    assert result["relevance"] >= 0.8
    assert result["fluency"] >= 0.7
    assert result["overall_score"] >= 0.75
```

#### 幻覺檢測測試

```python
def test_hallucination_detection():
    from ai_models.hallucination_detector import HallucinationDetector
    
    detector = HallucinationDetector()
    
    # 正確的資訊
    result = detector.detect(
        context="台灣的首都是台北。",
        response="台灣的首都是台北。"
    )
    assert result["is_hallucination"] == False
    
    # 錯誤的資訊（幻覺）
    result = detector.detect(
        context="台灣的首都是台北。",
        response="台灣的首都是高雄。"
    )
    assert result["is_hallucination"] == True
```

#### 模型漂移測試

```python
def test_model_drift():
    from ai_models.drift_monitor import DriftMonitor
    
    monitor = DriftMonitor()
    
    # 建立基準線
    baseline_responses = [
        "這是一個好問題...",
        "根據我的理解...",
        "讓我為您解釋..."
    ]
    for response in baseline_responses:
        monitor.add_baseline_response(response)
    
    # 測試新回應
    current_response = "這個問題很有趣..."
    result = monitor.detect_drift(current_response)
    
    assert "drift_score" in result
    assert result["drift_score"] >= 0.0
```

#### 偏見檢測測試

```python
def test_bias_detection():
    from ai_models.bias_detector import BiasDetector
    
    detector = BiasDetector()
    
    # 測試中性文本
    neutral_text = "這位工程師設計了一個優秀的系統。"
    result = detector.detect(neutral_text, categories=["gender"])
    assert result["bias_score"] < 0.3
    
    # 測試可能有偏見的文本
    biased_text = "女性護士通常比較溫柔。"
    result = detector.detect(biased_text, categories=["gender"])
    assert result["bias_score"] > 0.5
```

## 執行測試

### 基本執行

```bash
# 執行所有測試
pytest

# 詳細輸出
pytest -v

# 顯示測試輸出
pytest -s

# 平行執行（4個程序）
pytest -n 4
```

### 按類型執行

```bash
# 執行單元測試
pytest -m unit

# 執行整合測試
pytest -m integration

# 執行 AI 品質測試
pytest -m ai_quality

# 執行特定目錄
pytest tests/unit/
pytest tests/e2e/
```

### 覆蓋率報告

```bash
# 生成覆蓋率報告
pytest --cov=. --cov-report=html

# 只顯示未覆蓋的行
pytest --cov=. --cov-report=term-missing

# 指定最低覆蓋率
pytest --cov=. --cov-fail-under=80
```

### 使用監控

```bash
# 啟用 Console 追蹤
pytest --trace-console

# 啟用 Prometheus 指標
pytest --metrics-prometheus

# 啟用所有監控
pytest --trace-console --trace-otlp --metrics-prometheus
```

### 使用 Makefile

```bash
# 執行所有測試
make test

# 執行單元測試
make test-unit

# 執行整合測試
make test-integration

# 執行 AI 測試
make test-ai

# 生成覆蓋率報告
make coverage

# 執行所有檢查
make check-all
```

## 測試報告

### HTML 報告

```bash
# 生成 HTML 報告
pytest --html=report.html --self-contained-html

# 查看報告
# 打開 report.html 在瀏覽器中
```

### Allure 報告

```bash
# 生成 Allure 結果
pytest --alluredir=reports/allure

# 查看 Allure 報告
allure serve reports/allure
```

### 覆蓋率報告

```bash
# 生成覆蓋率報告
pytest --cov=. --cov-report=html

# 查看覆蓋率
# 打開 htmlcov/index.html
```

## 最佳實踐

### 1. 測試命名

```python
# 好的命名
def test_user_login_with_valid_credentials():
    pass

def test_chat_message_send_returns_response():
    pass

def test_ai_response_quality_meets_threshold():
    pass

# 避免的命名
def test_1():
    pass

def test_stuff():
    pass
```

### 2. 測試組織

```
tests/
├── unit/           # 快速、獨立的單元測試
├── integration/    # 元件互動測試
├── e2e/           # 完整流程測試（較慢）
├── ai_quality/    # AI 品質測試
└── llm_specific/  # LLM 特定測試
```

### 3. 使用 Fixtures

```python
# 好的做法：使用 fixture
@pytest.fixture
def chat_client():
    client = ChatClient()
    yield client
    client.close()

def test_with_client(chat_client):
    response = chat_client.send("Hello")
    assert response is not None

# 避免：在測試中重複設置
def test_without_fixture():
    client = ChatClient()  # 重複
    response = client.send("Hello")
    client.close()  # 重複
```

### 4. 獨立性

```python
# 好的做法：測試獨立
def test_feature_a():
    # 不依賴其他測試
    assert feature_a() == expected_a

def test_feature_b():
    # 不依賴 test_feature_a
    assert feature_b() == expected_b

# 避免：測試相互依賴
global_state = None

def test_setup():
    global global_state
    global_state = "setup"

def test_depends_on_setup():  # ❌ 依賴順序
    assert global_state == "setup"
```

### 5. 斷言清晰

```python
# 好的做法：清晰的斷言
def test_response_format():
    response = get_response()
    assert response["status"] == "success", "Response status should be success"
    assert "data" in response, "Response should contain data field"
    assert len(response["data"]) > 0, "Data should not be empty"

# 避免：模糊的斷言
def test_response():
    response = get_response()
    assert response  # 不清楚在測試什麼
```

### 6. 測試資料

```python
# 好的做法：使用測試資料檔案
def test_with_test_data(test_data_dir):
    with open(test_data_dir / "chat_messages.json") as f:
        test_cases = json.load(f)
    
    for case in test_cases:
        result = process(case["input"])
        assert result == case["expected"]

# 避免：硬編碼大量資料
def test_with_hardcoded_data():
    case1 = {"input": "...", "expected": "..."}
    case2 = {"input": "...", "expected": "..."}
    # ... 100 行資料
```

## 常見問題

### Q: 測試執行很慢怎麼辦？

**A:** 
1. 使用平行執行：`pytest -n 4`
2. 只執行特定測試：`pytest -m unit`
3. 跳過慢速測試：`pytest -m "not slow"`
4. 使用快取：`pytest --lf`（只執行上次失敗的）

### Q: 如何除錯失敗的測試？

**A:**
1. 使用 `-s` 查看輸出：`pytest -s`
2. 使用 `--pdb` 進入除錯：`pytest --pdb`
3. 查看詳細日誌：`pytest -v --log-cli-level=DEBUG`
4. 使用 VS Code 的測試除錯功能

### Q: 如何處理不穩定的測試？

**A:**
1. 找出根本原因（時序問題、資源競爭等）
2. 使用重試：`@pytest.mark.flaky(reruns=3)`
3. 增加等待時間：使用 `time.sleep()` 或 Playwright 的 `wait_for`
4. 隔離測試：確保測試之間沒有共享狀態

### Q: E2E 測試失敗但本地可以執行？

**A:**
1. 檢查環境差異（瀏覽器版本、網路等）
2. 確認測試資料在 CI 環境中可用
3. 增加超時時間
4. 使用 headless 模式：`pytest --headed`（查看瀏覽器）

### Q: 如何測試非同步程式碼？

**A:**
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

### Q: 如何模擬外部依賴？

**A:**
```python
from unittest.mock import Mock, patch

def test_with_mock():
    with patch('module.external_api') as mock_api:
        mock_api.return_value = {"status": "success"}
        result = function_that_calls_api()
        assert result["status"] == "success"
```

## 進階主題

### 測試資料生成

```bash
# 生成測試資料
python utils/test_data_generator.py

# 驗證測試資料
python utils/test_data_validator.py
```

### 監控與追蹤

參考 [MONITORING.md](MONITORING.md) 了解如何使用：
- OpenTelemetry 追蹤
- Prometheus 指標
- Grafana 視覺化

### 資料版本控制

參考 [DATA_MANAGEMENT.md](DATA_MANAGEMENT.md) 了解如何：
- 使用 DVC 追蹤測試資料
- 版本控制大型資料集
- 團隊協作

## 參考資源

- [Pytest 官方文件](https://docs.pytest.org/)
- [Playwright 文件](https://playwright.dev/python/)
- [測試金字塔](https://martinfowler.com/articles/practical-test-pyramid.html)
- [AI 測試最佳實踐](https://www.deeplearning.ai/the-batch/issue-233/)

## 總結

本測試框架提供：
- ✅ 多種測試類型支援
- ✅ 豐富的 Fixtures 和工具
- ✅ AI/LLM 專用測試工具
- ✅ 完整的監控和報告
- ✅ 資料版本控制

遵循本指南，您可以：
1. 快速編寫有效的測試
2. 組織和執行測試套件
3. 生成專業的測試報告
4. 維護高品質的測試程式碼

有問題？請查閱其他文件或提交 Issue！
