# SysTalk.Chat 自動化測試框架

> 一個針對 SysTalk.Chat 智能客服系統的企業級自動化測試框架，整合 AI/LLM 品質測試與完整的可觀測性監控

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()
[![Coverage](https://img.shields.io/badge/coverage-78%25-yellow)]()
[![Python](https://img.shields.io/badge/python-3.12-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

## ✨ 核心特性

### 🧪 全面的測試類型
- **單元測試**: 元件級別的功能驗證
- **整合測試**: 系統間協作測試
- **E2E 測試**: 完整用戶流程測試
- **AI 品質測試**: 回應品質、幻覺檢測
- **安全測試**: 提示注入、越獄攻擊防禦
- **效能測試**: 延遲、吞吐量基準測試

### 🤖 AI/LLM 專用測試工具
- **ResponseEvaluator**: 多維度回應品質評估
- **HallucinationDetector**: 幻覺與事實性檢測
- **DriftMonitor**: 模型行為漂移監控
- **BiasDetector**: 偏見與公平性檢測

### 📊 監控與可觀測性
- **OpenTelemetry 整合**: 分散式追蹤與指標收集
- **Prometheus 指標**: 測試執行與 AI 品質指標
- **Grafana Dashboard**: 即時視覺化儀表板
- **自動化警報**: 測試失敗與品質下降通知

### 🚀 CI/CD 整合
- **GitHub Actions**: 自動化測試流水線
- **Docker 支援**: 容器化測試環境
- **程式碼品質**: Black, Flake8, Pylint, MyPy, Bandit
- **安全掃描**: 依賴漏洞檢測

## 📁 專案結構

```
systalk-chat-test-framework/
├── tests/                      # 測試案例
│   ├── unit/                   # 單元測試
│   ├── integration/            # 整合測試
│   ├── e2e/                    # E2E 測試
│   ├── ai_quality/             # AI 品質測試
│   ├── llm_specific/           # LLM 專用測試
│   └── security/               # 安全測試
├── ai_models/                  # AI 測試工具
│   ├── response_evaluator.py  # 回應評估器
│   ├── hallucination_detector.py  # 幻覺檢測器
│   ├── drift_monitor.py        # 漂移監控器
│   └── bias_detector.py        # 偏見檢測器
├── monitoring/                 # 監控系統
│   ├── observability.py        # OpenTelemetry 整合
│   ├── pytest_plugin.py        # Pytest 監控插件
│   ├── ai_metrics_collector.py # AI 指標收集器
│   ├── prometheus.yml          # Prometheus 配置
│   ├── alerts.yml              # 警報規則
│   └── grafana-dashboard.json  # Grafana 儀表板
├── page_objects/               # 頁面物件模型
├── fixtures/                   # 測試 Fixtures
├── config/                     # 配置檔案
├── data/                       # 測試資料
├── reports/                    # 測試報告
└── docs/                       # 文件

## 🚀 快速開始

### 1. 環境需求

- Python 3.12+
- Node.js 18+ (Playwright)
- Docker (可選，用於 Prometheus/Grafana)

### 2. 安裝

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
playwright install
```

### 3. 運行測試

```bash
# 運行所有測試
pytest

# 運行特定類型的測試
pytest -m unit          # 單元測試
pytest -m integration   # 整合測試
pytest -m ai_quality    # AI 品質測試

# 運行測試並生成覆蓋率報告
pytest --cov=. --cov-report=html

# 啟用監控
pytest --trace-console --metrics-prometheus
```

### 4. 使用 Makefile

```bash
# 查看所有命令
make help

# 安裝依賴
make install

# 運行測試
make test

# 程式碼品質檢查
make lint

# 格式化程式碼
make format

# 運行所有檢查
make check-all
```

## 📊 監控系統

### 啟動 Prometheus

```bash
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  -v $(pwd)/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

訪問 http://localhost:9090

### 啟動 Grafana

```bash
docker run -d \
  --name grafana \
  -p 3000:3000 \
  grafana/grafana
```

訪問 http://localhost:3000 (admin/admin)

導入 Dashboard: `monitoring/grafana-dashboard.json`

詳細監控設定請參考 [MONITORING.md](docs/MONITORING.md)

## 🧪 AI 測試工具使用

### 回應品質評估

```python
from ai_models.response_evaluator import ResponseEvaluator

evaluator = ResponseEvaluator()
result = evaluator.evaluate(
    question="什麼是機器學習？",
    response="機器學習是人工智慧的一個分支..."
)
print(f"品質分數: {result['overall_score']}")
```

### 幻覺檢測

```python
from ai_models.hallucination_detector import HallucinationDetector

detector = HallucinationDetector()
result = detector.detect(
    context="蘋果公司成立於 1976 年",
    response="蘋果公司成立於 1990 年"
)
print(f"幻覺檢測: {result['is_hallucination']}")
```

### 模型漂移監控

```python
from ai_models.drift_monitor import DriftMonitor

monitor = DriftMonitor()
monitor.add_baseline_response(baseline_response)
result = monitor.detect_drift(current_response)
print(f"漂移檢測: {result['drift_detected']}")
```

### 偏見檢測

```python
from ai_models.bias_detector import BiasDetector

detector = BiasDetector()
result = detector.detect(
    text="應徵者的評估...",
    categories=["gender", "age"]
)
print(f"偏見分數: {result['bias_score']}")
```

## 📈 測試報告

測試完成後，報告會生成在以下位置：

- **HTML 報告**: `reports/html/index.html`
- **覆蓋率報告**: `reports/coverage/index.html`
- **Allure 報告**: `reports/allure/`

## 🔧 配置

### 環境配置

在 `config/environments/` 目錄下配置不同環境：

- `dev.yaml`: 開發環境
- `staging.yaml`: 預發布環境
- `prod.yaml`: 生產環境

### 測試配置

在 `pytest.ini` 中配置 pytest 選項

### 監控配置

在 `monitoring/` 目錄下配置監控系統

## 🤝 開發指南

### 程式碼風格

```bash
# 格式化程式碼
make format

# 檢查程式碼品質
make lint

# 類型檢查
make type-check

# 安全檢查
make security-check
```

### 提交前檢查

```bash
make check-all
```

## 📚 文件

- [監控整合指南](docs/MONITORING.md)
- [專案架構說明](docs/Demo_Project_Architecture.md)
- [學習路線圖](docs/Learning_Roadmap_and_Demo_Projects.md)

## 🎯 測試指標

| 指標 | 數值 |
|------|------|
| 測試總數 | 34 |
| 測試通過率 | 100% |
| 程式碼覆蓋率 | 78% |
| AI 工具數量 | 4 |
| 監控指標數 | 20+ |

## 🛠️ 技術棧

- **測試框架**: Pytest 7.4.3
- **UI 測試**: Playwright 1.40.0
- **AI/ML**: Transformers, PyTorch, NLTK, spaCy
- **監控**: OpenTelemetry, Prometheus, Grafana
- **CI/CD**: GitHub Actions, Docker
- **程式碼品質**: Black, Flake8, Pylint, MyPy, Bandit

## 📝 授權

MIT License

## 👤 作者

開發中...

## 🙏 致謝

感謝 TPIsoftware 提供專案靈感與需求
   ```