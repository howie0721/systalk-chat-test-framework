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
- **GitHub Actions**: 自動化測試流水線 (CI, Nightly, Release)
- **Docker 支援**: 容器化測試環境與部署
- **程式碼品質**: Black, Flake8, Pylint, MyPy, Bandit
- **安全掃描**: 依賴漏洞檢測與 SAST 分析

### 📦 測試資料管理
- **DVC 整合**: Git-like 的資料版本控制
- **測試資料生成**: 自動生成 560+ 測試案例
- **資料驗證**: 確保測試資料完整性與一致性
- **團隊協作**: 支援多人協作與資料共享

## 📁 專案結構

```
systalk-chat-test-framework/
├── tests/                      # 測試案例
│   ├── unit/                   # 單元測試
│   ├── integration/            # 整合測試
│   ├── e2e/                    # E2E 測試
│   ├── ai_quality/             # AI 品質測試
│   ├── ai_specific/            # AI 特定測試
│   ├── llm_specific/           # LLM 特定測試
│   ├── security/               # 安全測試
│   └── performance/            # 效能測試
├── ai_models/                  # AI 測試工具
│   ├── response_evaluator.py  # 回應評估器
│   ├── hallucination_detector.py  # 幻覺檢測器
│   ├── drift_monitor.py        # 漂移監控器
│   └── bias_detector.py        # 偏見檢測器
├── pages/                      # 頁面物件模型 (Page Object Model)
│   ├── base_page.py            # 基礎頁面類別
│   └── chat_page.py            # 聊天頁面
├── fixtures/                   # 測試 Fixtures
│   ├── api_fixtures.py         # API 測試 fixtures
│   └── browser_fixtures.py     # 瀏覽器測試 fixtures
├── monitoring/                 # 監控系統
│   ├── observability.py        # OpenTelemetry 整合
│   ├── pytest_plugin.py        # Pytest 監控插件
│   ├── ai_metrics_collector.py # AI 指標收集器
│   ├── prometheus/             # Prometheus 配置
│   └── grafana/                # Grafana 儀表板
├── utils/                      # 工具程式
│   ├── test_data_generator.py # 測試資料生成器
│   └── test_data_validator.py # 資料驗證器
├── config/                     # 配置檔案
│   ├── environments/           # 環境配置
│   └── *.yaml                  # YAML 配置檔
├── data/                       # 測試資料 (DVC 管理)
│   ├── test_datasets/          # 測試資料集
│   └── golden_datasets/        # 黃金標準資料集
├── docker/                     # Docker 相關檔案
├── .github/                    # GitHub Actions
│   └── workflows/              # CI/CD 工作流程
│       ├── ci.yml              # 持續整合
│       ├── nightly.yml         # 夜間測試
│       └── release.yml         # 發布流程
├── docs/                       # 完整文件 (6300+ 行)
│   ├── ARCHITECTURE.md         # 系統架構
│   ├── API.md                  # API 文件
│   ├── TESTING_GUIDE.md        # 測試指南
│   ├── MONITORING_GUIDE.md     # 監控指南
│   ├── CI_CD_GUIDE.md          # CI/CD 指南
│   ├── DATA_MANAGEMENT.md      # 資料管理指南
│   ├── SECURITY.md             # 安全最佳實踐
│   ├── CONTRIBUTING.md         # 貢獻指南
│   ├── DEMO_GUIDE.md           # Demo 展示指南
│   ├── INTERVIEW_PREP.md       # 面試準備指南
│   └── PORTFOLIO_GUIDE.md      # 作品集指南
├── conftest.py                 # Pytest 全局配置
├── pytest.ini                  # Pytest 配置
├── pyproject.toml              # 專案元數據
├── Dockerfile                  # Docker 映像
├── docker-compose.yml          # Docker Compose
├── Makefile                    # 開發命令 (35+ 命令)
├── dvc.yaml                    # DVC 管道
├── requirements.txt            # Python 依賴
└── PROJECT_COMPLETION_REPORT.md # 專案完成報告

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

### 使用 Docker Compose 啟動 (推薦)

```bash
# 啟動 Prometheus + Grafana
docker-compose up -d

# 查看狀態
docker-compose ps

# 停止服務
docker-compose down
```

### 訪問監控介面

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

### 配置 Grafana

1. 登入 Grafana
2. 添加 Prometheus 資料源 (http://prometheus:9090)
3. 導入 Dashboard: `monitoring/grafana_dashboard.json`

### 查看測試指標

運行測試時啟用監控：

```bash
# 啟用 OpenTelemetry 追蹤
pytest --trace-console

# 啟用 Prometheus 指標
pytest --metrics-prometheus

# 同時啟用兩者
pytest --trace-console --metrics-prometheus
```

詳細監控設定請參考 [MONITORING.md](docs/MONITORING.md)

## 🧪 AI 測試工具使用

### ResponseEvaluator - 回應品質評估

```python
from ai_models.response_evaluator import ResponseEvaluator

evaluator = ResponseEvaluator()
result = evaluator.evaluate(
    question="什麼是機器學習？",
    response="機器學習是人工智慧的一個分支，讓電腦能從資料中學習..."
)

print(f"連貫性: {result['coherence']:.2f}")
print(f"相關性: {result['relevance']:.2f}")
print(f"流暢度: {result['fluency']:.2f}")
print(f"完整性: {result['completeness']:.2f}")
print(f"總分: {result['overall_score']:.2f}")
```

### HallucinationDetector - 幻覺檢測

```python
from ai_models.hallucination_detector import HallucinationDetector

detector = HallucinationDetector()
result = detector.detect(
    context="蘋果公司成立於 1976 年，由 Steve Jobs、Steve Wozniak 和 Ronald Wayne 創立。",
    response="蘋果公司成立於 1990 年，由 Bill Gates 創立。"
)

print(f"是否為幻覺: {result['is_hallucination']}")
print(f"風險等級: {result['risk_level']}")
print(f"矛盾內容: {result['contradictions']}")
print(f"未支持聲明: {result['unsupported_claims']}")
```

### DriftMonitor - 模型漂移監控

```python
from ai_models.drift_monitor import DriftMonitor

monitor = DriftMonitor(window_size=100)

# 建立基準
for response in baseline_responses:
    monitor.add_baseline_response(response, metadata={"version": "1.0"})

# 檢測漂移
result = monitor.detect_drift(
    current_response,
    metadata={"version": "2.0"}
)

print(f"漂移檢測: {result['drift_detected']}")
print(f"漂移分數: {result['drift_score']:.2f}")
print(f"嚴重程度: {result['severity']}")
print(f"變化百分比: {result['change_percentage']:.1f}%")
```

### BiasDetector - 偏見檢測

```python
from ai_models.bias_detector import BiasDetector

detector = BiasDetector()
result = detector.detect(
    text="這個職位更適合年輕男性，因為需要經常加班...",
    categories=["gender", "age"]
)

print(f"偏見檢測: {result['bias_detected']}")
print(f"偏見分數: {result['bias_score']:.2f}")
print(f"公平性分數: {result['fairness_score']:.2f}")
print(f"偏見類型: {result['bias_types']}")
print(f"問題短語: {result['problematic_phrases']}")
print(f"改善建議: {result['recommendations']}")
```

完整 API 文件請參考 [API.md](docs/API.md)

## 📈 測試報告

### 生成報告

```bash
# HTML 測試報告
pytest --html=reports/html/report.html --self-contained-html

# 覆蓋率報告
pytest --cov=. --cov-report=html:reports/coverage

# Allure 報告
pytest --alluredir=reports/allure
allure serve reports/allure
```

### 報告位置

測試完成後，報告會生成在以下位置：

- **HTML 報告**: `reports/html/report.html`
- **覆蓋率報告**: `reports/coverage/index.html`
- **Allure 報告**: `reports/allure/`
- **JUnit XML**: `reports/junit/junit.xml`

### 查看報告

```bash
# 在瀏覽器中打開覆蓋率報告
make coverage-report

# 使用 Allure 查看測試報告
allure serve reports/allure
```

## 🔧 配置

### 環境變數

創建 `.env` 檔案：

```bash
# 應用配置
APP_ENV=development
BASE_URL=https://systalk.chat

# 監控配置
OTLP_ENDPOINT=http://localhost:4317
PROMETHEUS_PORT=8000

# AI 模型配置
MODEL_NAME=gpt-4
MAX_TOKENS=2000
TEMPERATURE=0.7
```

### 測試配置

`pytest.ini` 配置選項：

```ini
[pytest]
# 測試目錄
testpaths = tests

# 標記
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    ai_quality: AI quality tests
    security: Security tests
    slow: Slow running tests

# 輸出選項
addopts = 
    -v
    --strict-markers
    --cov=.
    --cov-report=html
    --cov-report=term-missing
```

### 監控配置

在 `config/config.yaml` 中配置監控選項：

```yaml
monitoring:
  enabled: true
  console_exporter: true
  prometheus_exporter: true
  otlp_exporter: false
```

## 🤝 開發指南

### 開發環境設置

```bash
# 安裝開發依賴
make install-dev

# 安裝 pre-commit hooks
pre-commit install

# 運行 pre-commit 檢查
pre-commit run --all-files
```

### 程式碼風格

本專案遵循以下程式碼規範：

- **PEP 8**: Python 風格指南
- **Black**: 程式碼格式化 (行長度 127)
- **isort**: Import 排序
- **Type Hints**: 使用型別標註

```bash
# 自動格式化程式碼
make format

# 檢查程式碼品質
make lint

# 類型檢查
make type-check

# 安全檢查
make security-check
```

### 測試要求

- 新功能必須包含測試
- 測試覆蓋率目標：80%+
- 所有測試必須通過
- 遵循 AAA 模式 (Arrange-Act-Assert)

### 提交前檢查

```bash
# 運行所有檢查
make check-all

# 檢查內容包括：
# - 程式碼格式化
# - 程式碼品質檢查
# - 型別檢查
# - 安全檢查
# - 測試執行
# - 覆蓋率檢查
```

### Git 工作流程

```bash
# 創建功能分支
git checkout -b feature/your-feature

# 提交變更
git add .
git commit -m "feat: add new feature"

# 推送並創建 Pull Request
git push origin feature/your-feature
```

詳細貢獻指南請參考 [CONTRIBUTING.md](docs/CONTRIBUTING.md)

## 📚 完整文件

### 核心文件

- **[系統架構](docs/ARCHITECTURE.md)**: 系統設計、元件說明、技術決策
- **[API 文件](docs/API.md)**: 完整 API 參考與使用範例
- **[測試指南](docs/TESTING_GUIDE.md)**: 測試類型、寫法、執行方式
- **[監控指南](docs/MONITORING.md)**: OpenTelemetry、Prometheus、Grafana 整合
- **[資料管理](docs/DATA_MANAGEMENT.md)**: DVC 使用、資料生成與驗證
- **[貢獻指南](docs/CONTRIBUTING.md)**: 如何貢獻程式碼、開發流程

### 專案規劃

- [專案架構說明](docs/Demo_Project_Architecture.md)
- [學習路線圖](docs/Learning_Roadmap_and_Demo_Projects.md)

### 快速導航

| 想要... | 查看 |
|--------|------|
| 了解系統架構 | [ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| 查詢 API 用法 | [API.md](docs/API.md) |
| 學習寫測試 | [TESTING_GUIDE.md](docs/TESTING_GUIDE.md) |
| 設置監控 | [MONITORING.md](docs/MONITORING.md) |
| 管理測試資料 | [DATA_MANAGEMENT.md](docs/DATA_MANAGEMENT.md) |
| 貢獻程式碼 | [CONTRIBUTING.md](docs/CONTRIBUTING.md) |

## 🎯 專案成果

### 測試指標

| 指標 | 數值 |
|------|------|
| 測試總數 | 34 |
| 測試通過率 | 100% |
| 程式碼覆蓋率 | 78% |
| AI 工具數量 | 4 |
| 監控指標數 | 20+ |
| 測試資料筆數 | 560 |
| Makefile 命令 | 35+ |

### 功能完成度

- ✅ 單元測試框架
- ✅ 整合測試框架
- ✅ E2E 測試框架
- ✅ AI 品質測試工具 (4 個)
- ✅ 監控與觀測系統
- ✅ CI/CD 流水線 (3 個 workflows)
- ✅ Docker 容器化
- ✅ 測試資料管理 (DVC)
- ✅ 完整文件系統
- ✅ 程式碼品質工具

### 技術亮點

- 🚀 完整的 AI/LLM 測試工具鏈
- 📊 端到端的監控與可觀測性
- 🔄 自動化 CI/CD 流水線
- 📦 專業的測試資料管理
- 📚 完善的文件系統
- 🐳 容器化部署支援

## 🛠️ 技術棧

### 核心框架

- **測試框架**: Pytest 7.4.3
- **UI 測試**: Playwright 1.40.0
- **Python**: 3.12.2

### AI/ML 工具

- **NLP**: spaCy 3.7.2, NLTK 3.8.1
- **深度學習**: PyTorch 2.9.0, Transformers 4.35.2

### 監控系統

- **觀測性**: OpenTelemetry SDK 1.38.0
- **指標**: Prometheus
- **視覺化**: Grafana

### DevOps

- **版本控制**: Git, DVC 3.50.0
- **CI/CD**: GitHub Actions
- **容器化**: Docker, Docker Compose

### 程式碼品質

- **格式化**: Black 23.12.1, isort 5.13.2
- **檢查**: Flake8 7.0.0, Pylint 3.0.3
- **型別檢查**: MyPy 1.8.0
- **安全**: Bandit 1.7.6

## 📝 授權

MIT License

## 👤 作者

開發中...

## 🙏 致謝

感謝 TPIsoftware 提供專案靈感與需求
   ```