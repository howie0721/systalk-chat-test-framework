# API 文件

## AI 測試工具 API

### ResponseEvaluator

評估 AI 回應的品質。

#### 類別初始化

```python
from ai_models.response_evaluator import ResponseEvaluator

evaluator = ResponseEvaluator()
```

#### 方法

##### `evaluate(question: str, response: str, context: str = None) -> Dict[str, Any]`

評估回應的整體品質。

**參數：**
- `question` (str): 使用者的問題
- `response` (str): AI 的回應
- `context` (str, optional): 上下文資訊

**返回：**
```python
{
    "coherence": float,      # 連貫性分數 (0-1)
    "relevance": float,      # 相關性分數 (0-1)
    "fluency": float,        # 流暢度分數 (0-1)
    "completeness": float,   # 完整性分數 (0-1)
    "overall_score": float,  # 總分 (0-1)
    "details": dict          # 詳細評估資訊
}
```

**範例：**
```python
result = evaluator.evaluate(
    question="什麼是機器學習？",
    response="機器學習是人工智慧的一個分支，致力於開發能夠從資料中學習的演算法。"
)
print(f"整體分數: {result['overall_score']:.2f}")
```

##### `evaluate_coherence(question: str, response: str) -> Dict[str, float]`

評估回應的連貫性。

**參數：**
- `question` (str): 使用者的問題
- `response` (str): AI 的回應

**返回：**
```python
{
    "score": float,          # 連貫性分數 (0-1)
    "sentence_coherence": float,  # 句子連貫性
    "logical_flow": float    # 邏輯流暢度
}
```

##### `evaluate_relevance(question: str, response: str) -> Dict[str, float]`

評估回應的相關性。

**參數：**
- `question` (str): 使用者的問題
- `response` (str): AI 的回應

**返回：**
```python
{
    "score": float,          # 相關性分數 (0-1)
    "keyword_match": float,  # 關鍵字匹配度
    "topic_alignment": float # 主題對齊度
}
```

---

### HallucinationDetector

檢測 AI 回應中的幻覺（虛假資訊）。

#### 類別初始化

```python
from ai_models.hallucination_detector import HallucinationDetector

detector = HallucinationDetector()
```

#### 方法

##### `detect(context: str, response: str, reference: str = None) -> Dict[str, Any]`

檢測回應中的幻覺。

**參數：**
- `context` (str): 真實的上下文或事實
- `response` (str): AI 的回應
- `reference` (str, optional): 參考答案

**返回：**
```python
{
    "is_hallucination": bool,      # 是否為幻覺
    "confidence": float,           # 信心度 (0-1)
    "risk_level": str,            # 風險等級: low/medium/high/critical
    "contradictions": List[str],  # 發現的矛盾
    "unsupported_claims": List[str],  # 無根據的聲稱
    "factual_accuracy": float     # 事實準確度 (0-1)
}
```

**範例：**
```python
result = detector.detect(
    context="台灣的首都是台北。",
    response="台灣的首都是高雄。"
)
if result["is_hallucination"]:
    print(f"警告：檢測到幻覺！風險等級：{result['risk_level']}")
```

##### `check_factual_consistency(statements: List[str], facts: List[str]) -> Dict[str, Any]`

檢查陳述與事實的一致性。

**參數：**
- `statements` (List[str]): 要檢查的陳述列表
- `facts` (List[str]): 已知事實列表

**返回：**
```python
{
    "consistency_score": float,    # 一致性分數 (0-1)
    "inconsistent_statements": List[str],  # 不一致的陳述
    "supported_statements": List[str]      # 有支持的陳述
}
```

---

### DriftMonitor

監控 AI 模型的行為漂移。

#### 類別初始化

```python
from ai_models.drift_monitor import DriftMonitor

monitor = DriftMonitor(window_size=100)
```

**參數：**
- `window_size` (int): 滑動視窗大小，預設 100

#### 方法

##### `add_baseline_response(response: str, metadata: Dict = None) -> None`

添加基準線回應。

**參數：**
- `response` (str): 基準線回應
- `metadata` (Dict, optional): 相關元資料

**範例：**
```python
monitor.add_baseline_response("這是一個標準的回應格式...")
```

##### `detect_drift(current_response: str, metadata: Dict = None) -> Dict[str, Any]`

檢測當前回應是否漂移。

**參數：**
- `current_response` (str): 當前的回應
- `metadata` (Dict, optional): 相關元資料

**返回：**
```python
{
    "drift_detected": bool,       # 是否檢測到漂移
    "drift_score": float,         # 漂移分數 (0-1)
    "severity": str,             # 嚴重程度: low/medium/high
    "change_percentage": float,   # 變化百分比
    "affected_features": List[str],  # 受影響的特徵
    "timestamp": str             # 時間戳記
}
```

**範例：**
```python
result = monitor.detect_drift("新的回應模式...")
if result["drift_detected"]:
    print(f"漂移嚴重程度: {result['severity']}")
    print(f"變化百分比: {result['change_percentage']:.1f}%")
```

##### `get_drift_history(limit: int = 100) -> List[Dict[str, Any]]`

獲取漂移歷史記錄。

**參數：**
- `limit` (int): 返回的最大記錄數

**返回：**
```python
[
    {
        "timestamp": str,
        "drift_score": float,
        "severity": str,
        ...
    },
    ...
]
```

##### `reset_baseline() -> None`

重置基準線。

---

### BiasDetector

檢測 AI 回應中的偏見。

#### 類別初始化

```python
from ai_models.bias_detector import BiasDetector

detector = BiasDetector()
```

#### 方法

##### `detect(text: str, categories: List[str] = None) -> Dict[str, Any]`

檢測文本中的偏見。

**參數：**
- `text` (str): 要檢測的文本
- `categories` (List[str], optional): 偏見類別，可選：
  - `"gender"`: 性別偏見
  - `"age"`: 年齡偏見
  - `"race"`: 種族偏見
  - `"occupation"`: 職業偏見
  
  如果未指定，檢測所有類別。

**返回：**
```python
{
    "bias_detected": bool,        # 是否檢測到偏見
    "bias_score": float,         # 偏見分數 (0-1)
    "fairness_score": float,     # 公平性分數 (0-1)
    "bias_types": {              # 各類別的偏見分數
        "gender": float,
        "age": float,
        "race": float,
        "occupation": float
    },
    "problematic_phrases": List[str],  # 有問題的片段
    "recommendations": List[str]       # 改進建議
}
```

**範例：**
```python
result = detector.detect(
    text="護士通常是女性，醫生通常是男性。",
    categories=["gender"]
)
if result["bias_detected"]:
    print(f"檢測到性別偏見，分數: {result['bias_types']['gender']:.2f}")
    print("建議:", result["recommendations"])
```

##### `compare_responses(response_a: str, response_b: str) -> Dict[str, Any]`

比較兩個回應的偏見差異。

**參數：**
- `response_a` (str): 第一個回應
- `response_b` (str): 第二個回應

**返回：**
```python
{
    "bias_difference": float,    # 偏見差異
    "fairness_comparison": str,  # 公平性比較: better/worse/equal
    "details": dict             # 詳細比較資訊
}
```

---

## 頁面物件 API

### BasePage

所有頁面物件的基礎類別。

#### 類別初始化

```python
from pages.base_page import BasePage

page = BasePage(playwright_page)
```

**參數：**
- `playwright_page`: Playwright 的 Page 物件

#### 方法

##### `navigate(url: str) -> None`

導航到指定 URL。

##### `wait_for_selector(selector: str, timeout: int = 30000) -> None`

等待元素出現。

##### `click(selector: str) -> None`

點擊元素。

##### `fill(selector: str, text: str) -> None`

填寫表單。

##### `get_text(selector: str) -> str`

獲取元素文本。

---

### ChatPage

聊天頁面的專用操作。

#### 類別初始化

```python
from pages.chat_page import ChatPage

chat_page = ChatPage(playwright_page)
```

#### 方法

##### `navigate() -> None`

導航到聊天頁面。

##### `send_message(message: str) -> None`

發送聊天訊息。

**參數：**
- `message` (str): 要發送的訊息

**範例：**
```python
chat_page.send_message("你好，我需要幫助")
```

##### `get_last_response() -> str`

獲取最後一條回應。

**返回：**
- `str`: 最後的回應文本

##### `wait_for_response(timeout: int = 30000) -> bool`

等待回應出現。

**參數：**
- `timeout` (int): 超時時間（毫秒）

**返回：**
- `bool`: 是否成功接收到回應

##### `clear_chat() -> None`

清空聊天歷史。

---

## 工具類 API

### TestDataGenerator

生成測試資料。

#### 類別初始化

```python
from utils.test_data_generator import TestDataGenerator

generator = TestDataGenerator(seed=42)
```

**參數：**
- `seed` (int): 隨機種子，用於可重現的資料生成

#### 方法

##### `generate_chat_messages(count: int = 100) -> List[Dict]`

生成聊天訊息資料。

**參數：**
- `count` (int): 要生成的訊息數量

**返回：**
```python
[
    {
        "message_id": str,
        "user_id": str,
        "message": str,
        "intent": str,
        "timestamp": str,
        "channel": str,
        "session_id": str
    },
    ...
]
```

##### `generate_ai_test_cases(count: int = 50) -> List[Dict]`

生成 AI 測試案例。

##### `save_to_file(data: List[Dict], filepath: Path) -> None`

儲存資料到檔案。

---

### TestDataValidator

驗證測試資料。

#### 類別初始化

```python
from utils.test_data_validator import TestDataValidator

validator = TestDataValidator()
```

#### 方法

##### `validate_file(filepath: Path, data_type: str) -> bool`

驗證檔案。

**參數：**
- `filepath` (Path): 檔案路徑
- `data_type` (str): 資料類型，可選：
  - `"chat_messages"`
  - `"ai_test_cases"`
  - `"prompt_injection_cases"`
  - `"bias_test_cases"`
  - `"performance_test_data"`

**返回：**
- `bool`: 驗證是否通過

**範例：**
```python
is_valid = validator.validate_file(
    Path("data/test_datasets/chat_messages.json"),
    "chat_messages"
)
if not is_valid:
    print("驗證失敗:", validator.validation_errors)
```

##### `validate_all_datasets(data_dir: Path) -> bool`

驗證所有資料集。

---

## 監控 API

### TestObservability

測試可觀測性。

#### 獲取實例

```python
from monitoring.observability import get_observability

observability = get_observability(
    service_name="my-service",
    enable_console=True,
    enable_otlp=False,
    enable_prometheus=True
)
```

#### 方法

##### `create_span(name: str, attributes: Dict = None) -> ContextManager`

創建追蹤 Span。

**範例：**
```python
with observability.create_span("test_operation", {"test.id": "123"}):
    # 執行操作
    result = perform_test()
```

##### `record_test_metric(test_name: str, status: str, duration: float) -> None`

記錄測試指標。

##### `record_ai_metric(model_name: str, metric_name: str, value: float, labels: Dict = None) -> None`

記錄 AI 指標。

---

### AIMetricsCollector

AI 指標收集器。

#### 獲取實例

```python
from monitoring.ai_metrics_collector import get_ai_metrics_collector

collector = get_ai_metrics_collector()
```

#### 方法

##### `record_response_quality(model_name: str, metrics: Dict) -> None`

記錄回應品質指標。

**範例：**
```python
collector.record_response_quality(
    model_name="gpt-4",
    metrics={
        "coherence": 0.85,
        "relevance": 0.90,
        "overall_score": 0.88
    }
)
```

##### `record_hallucination_detection(model_name: str, detection_result: Dict) -> None`

記錄幻覺檢測結果。

##### `record_drift_detection(model_name: str, drift_result: Dict) -> None`

記錄漂移檢測結果。

##### `record_bias_detection(model_name: str, bias_result: Dict) -> None`

記錄偏見檢測結果。

---

## 使用範例

### 完整的測試流程

```python
import pytest
from ai_models.response_evaluator import ResponseEvaluator
from monitoring.ai_metrics_collector import get_ai_metrics_collector

@pytest.mark.ai_quality
def test_ai_response_quality():
    # 初始化
    evaluator = ResponseEvaluator()
    collector = get_ai_metrics_collector()
    
    # 測試資料
    question = "什麼是深度學習？"
    response = "深度學習是機器學習的一個子領域..."
    
    # 評估
    result = evaluator.evaluate(question, response)
    
    # 記錄指標
    collector.record_response_quality(
        model_name="test-model",
        metrics=result
    )
    
    # 斷言
    assert result["overall_score"] >= 0.7
    assert result["relevance"] >= 0.8
```

### 結合多個工具

```python
def test_comprehensive_ai_check():
    from ai_models.response_evaluator import ResponseEvaluator
    from ai_models.hallucination_detector import HallucinationDetector
    from ai_models.bias_detector import BiasDetector
    
    response = "AI 生成的回應..."
    context = "相關上下文..."
    
    # 品質評估
    evaluator = ResponseEvaluator()
    quality = evaluator.evaluate("問題", response)
    
    # 幻覺檢測
    hallucination_detector = HallucinationDetector()
    hallucination = hallucination_detector.detect(context, response)
    
    # 偏見檢測
    bias_detector = BiasDetector()
    bias = bias_detector.detect(response)
    
    # 綜合判斷
    assert quality["overall_score"] >= 0.7
    assert not hallucination["is_hallucination"]
    assert bias["bias_score"] < 0.3
```

## 錯誤處理

所有 API 方法在遇到錯誤時會拋出適當的異常：

- `ValueError`: 參數無效
- `FileNotFoundError`: 檔案不存在
- `RuntimeError`: 執行時錯誤

建議使用 try-except 處理：

```python
try:
    result = evaluator.evaluate(question, response)
except ValueError as e:
    print(f"參數錯誤: {e}")
except Exception as e:
    print(f"未預期的錯誤: {e}")
```

## 版本相容性

- Python: 3.12+
- Playwright: 1.40+
- Pytest: 7.4+

## 更多資源

- [測試指南](TESTING_GUIDE.md)
- [監控指南](MONITORING.md)
- [資料管理](DATA_MANAGEMENT.md)
