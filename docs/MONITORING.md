# 監控整合指南

## 概述

本測試框架整合了 OpenTelemetry、Prometheus 和 Grafana，提供全面的測試執行和 AI 品質監控。

## 架構

```
監控系統架構:
┌─────────────────┐
│  Test Framework │
│   (OpenTelemetry)│
└────────┬────────┘
         │
         ├─→ Console Export (開發環境)
         ├─→ OTLP Export (Jaeger/Tempo)
         └─→ Prometheus Metrics
                  │
         ┌────────▼────────┐
         │   Prometheus    │
         │  (指標收集)      │
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │     Grafana     │
         │  (視覺化儀表板)  │
         └─────────────────┘
```

## 快速開始

### 1. 安裝依賴

監控相關套件已包含在 `requirements.txt` 中：

```bash
pip install -r requirements.txt
```

主要套件：
- `opentelemetry-sdk`: OpenTelemetry 核心
- `opentelemetry-exporter-otlp`: OTLP 匯出器
- `opentelemetry-instrumentation-requests`: HTTP 請求追蹤
- `prometheus-client`: Prometheus 指標

### 2. 運行測試並啟用監控

```bash
# 啟用 Console 追蹤（開發環境）
pytest --trace-console

# 啟用 Prometheus 指標（生產環境）
pytest --metrics-prometheus

# 啟用所有監控
pytest --trace-console --trace-otlp --metrics-prometheus
```

### 3. 啟動 Prometheus（可選）

```bash
# 使用 Docker 啟動 Prometheus
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  -v $(pwd)/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# 訪問 http://localhost:9090
```

### 4. 查看 Grafana Dashboard（可選）

```bash
# 使用 Docker 啟動 Grafana
docker run -d \
  --name grafana \
  -p 3000:3000 \
  grafana/grafana

# 訪問 http://localhost:3000
# 預設帳號: admin / admin
```

導入儀表板：
1. 登入 Grafana
2. Configuration → Data Sources → Add Prometheus
3. Dashboards → Import → 上傳 `monitoring/grafana-dashboard.json`

## 監控功能

### 1. 測試執行監控

自動收集的指標：

- **test_executions_total**: 測試執行次數（按狀態分類）
- **test_duration_seconds**: 測試執行時間直方圖
- **test_session_duration**: 測試會話總時長

追蹤資訊：
- 每個測試的 Span
- 測試會話的 Span
- 詳細的屬性（檔案、行號、函數名稱）

### 2. AI 品質監控

使用 `AIMetricsCollector` 收集：

```python
from monitoring.ai_metrics_collector import get_ai_metrics_collector

collector = get_ai_metrics_collector()

# 記錄回應品質
collector.record_response_quality(
    model_name="gpt-4",
    metrics={
        "coherence": 0.85,
        "relevance": 0.90,
        "fluency": 0.88,
        "overall_score": 0.88
    }
)

# 記錄幻覺檢測
collector.record_hallucination_detection(
    model_name="gpt-4",
    detection_result={
        "is_hallucination": False,
        "confidence": 0.92,
        "risk_level": "low"
    }
)

# 記錄模型漂移
collector.record_drift_detection(
    model_name="gpt-4",
    drift_result={
        "drift_detected": True,
        "drift_score": 0.35,
        "severity": "medium"
    }
)

# 記錄偏見檢測
collector.record_bias_detection(
    model_name="gpt-4",
    bias_result={
        "bias_detected": False,
        "bias_score": 0.12,
        "fairness_score": 0.88
    }
)
```

### 3. 效能監控

```python
# 記錄效能指標
collector.record_performance_metrics(
    model_name="gpt-4",
    metrics={
        "latency": 1250,  # ms
        "token_count": 500,
        "cost": 0.015,  # USD
        "throughput": 400  # tokens/s
    }
)
```

### 4. 分散式追蹤

```python
from monitoring.observability import get_observability

observability = get_observability()

# 手動建立追蹤 Span
with observability.create_span(
    "custom_operation",
    attributes={
        "operation.type": "ai_inference",
        "model.name": "gpt-4"
    }
) as span:
    # 執行操作
    result = perform_ai_operation()
    span.set_attribute("result.success", True)
```

## 環境變數配置

```bash
# OpenTelemetry 服務名稱
export OTEL_SERVICE_NAME="systalk-test-framework"

# 環境
export OTEL_RESOURCE_ATTRIBUTES="environment=production"

# OTLP 匯出端點（Grafana Cloud / Jaeger）
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"

# 啟用 OTLP 匯出
export ENABLE_OTLP="true"

# 啟用 Prometheus 匯出
export ENABLE_PROMETHEUS="true"

# Prometheus 埠
export PROMETHEUS_PORT="9464"
```

## 指標說明

### 測試執行指標

| 指標名稱 | 類型 | 說明 |
|---------|------|------|
| `test_executions_total` | Counter | 測試執行總次數，標籤：test.name, test.status |
| `test_duration_seconds` | Histogram | 測試執行時間分佈 |

### AI 品質指標

| 指標名稱 | 類型 | 說明 |
|---------|------|------|
| `response_quality.overall` | Gauge | 整體回應品質分數 (0-1) |
| `response_quality.coherence` | Gauge | 連貫性分數 (0-1) |
| `response_quality.relevance` | Gauge | 相關性分數 (0-1) |
| `response_quality.fluency` | Gauge | 流暢度分數 (0-1) |
| `hallucination.detected` | Gauge | 幻覺檢測標記 (0/1) |
| `hallucination.confidence` | Gauge | 幻覺檢測信心度 (0-1) |
| `drift.detected` | Gauge | 模型漂移檢測標記 (0/1) |
| `drift.score` | Gauge | 漂移分數 (0-1) |
| `bias.detected` | Gauge | 偏見檢測標記 (0/1) |
| `bias.score` | Gauge | 偏見分數 (0-1) |
| `bias.fairness_score` | Gauge | 公平性分數 (0-1) |

### 效能指標

| 指標名稱 | 類型 | 說明 |
|---------|------|------|
| `performance.latency` | Gauge | AI 模型延遲 (ms) |
| `performance.token_count` | Gauge | Token 使用量 |
| `performance.cost` | Gauge | API 呼叫成本 (USD) |

## 警報規則

Prometheus 警報規則已配置於 `monitoring/alerts.yml`：

### 測試執行警報
- **HighTestFailureRate**: 測試失敗率 > 20%
- **SlowTestExecution**: 95th 百分位測試時間 > 60s
- **NoTestsExecuted**: 10 分鐘內無測試執行

### AI 品質警報
- **HighHallucinationRate**: 幻覺檢測率 > 30%
- **LowResponseQuality**: 平均品質分數 < 0.6
- **ModelDriftDetected**: 模型漂移檢測率 > 50%
- **BiasDetected**: 偏見檢測率 > 40%

### 效能警報
- **HighAILatency**: AI 延遲 > 5s
- **HighTokenUsage**: Token 使用率 > 10,000/5min

## Grafana 儀表板

預設儀表板包含以下面板：

### 測試執行區
1. **Test Execution Rate**: 測試執行速率趨勢
2. **Test Success Rate**: 測試成功率統計
3. **Active Tests**: 當前活躍測試數
4. **Test Duration (95th Percentile)**: 測試時長百分位數
5. **Test Duration Heatmap**: 測試時長熱圖

### AI 品質區
6. **Response Quality Score**: 回應品質儀表盤
7. **Hallucination Detection Rate**: 幻覺檢測率儀表盤
8. **Model Drift Score**: 模型漂移分數儀表盤
9. **Bias Detection Score**: 偏見檢測分數儀表盤
10. **AI Quality Metrics Over Time**: AI 品質指標趨勢

### 效能區
11. **AI Model Latency**: AI 模型延遲趨勢
12. **Token Usage Rate**: Token 使用率趨勢

## 整合到 CI/CD

在 GitHub Actions 中使用監控：

```yaml
- name: Run tests with monitoring
  run: |
    pytest \
      --trace-console \
      --metrics-prometheus \
      --cov=. \
      --cov-report=html
  env:
    ENABLE_OTLP: "true"
    OTEL_EXPORTER_OTLP_ENDPOINT: ${{ secrets.OTEL_ENDPOINT }}
```

## 疑難排解

### 問題：Prometheus 無法連接到指標端點

**解決方案：**
1. 確認測試已使用 `--metrics-prometheus` 選項執行
2. 檢查 Prometheus 配置中的 targets 是否正確
3. 驗證端口 9464 沒有被防火牆阻擋

```bash
# 測試指標端點
curl http://localhost:9464/metrics
```

### 問題：OTLP 匯出失敗

**解決方案：**
1. 確認 OTLP 收集器正在運行（Jaeger/Tempo）
2. 檢查環境變數 `OTEL_EXPORTER_OTLP_ENDPOINT`
3. 查看錯誤日誌

```bash
# 啟動 Jaeger（用於測試）
docker run -d \
  --name jaeger \
  -p 16686:16686 \
  -p 4317:4317 \
  jaegertracing/all-in-one:latest
```

### 問題：指標沒有顯示在 Grafana

**解決方案：**
1. 確認 Prometheus 資料源配置正確
2. 檢查查詢語法是否正確
3. 驗證 Prometheus 正在抓取指標

```promql
# 測試查詢
rate(test_executions_total[5m])
```

## 最佳實踐

### 1. 開發環境
- 使用 `--trace-console` 進行即時除錯
- 不需要啟動外部服務

### 2. CI/CD 環境
- 使用 `--trace-otlp` 將追蹤傳送到集中式收集器
- 使用 `--metrics-prometheus` 收集長期指標

### 3. 生產環境
- 啟用所有監控選項
- 配置警報規則
- 定期審查 Grafana 儀表板

### 4. 效能考量
- 監控會增加少量開銷（通常 < 5%）
- 可以透過環境變數選擇性啟用功能
- Span 採樣可以減少追蹤數據量（在高負載環境中）

## 進階配置

### 自訂 Span Processor

```python
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# 自訂批次大小和延遲
processor = BatchSpanProcessor(
    span_exporter,
    max_queue_size=2048,
    schedule_delay_millis=5000,
    max_export_batch_size=512
)
```

### 自訂指標匯出間隔

```python
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

reader = PeriodicExportingMetricReader(
    exporter=console_exporter,
    export_interval_millis=30000  # 30 秒
)
```

## 參考資源

- [OpenTelemetry Python 文件](https://opentelemetry.io/docs/instrumentation/python/)
- [Prometheus 查詢語言](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Grafana Dashboard 最佳實踐](https://grafana.com/docs/grafana/latest/best-practices/)
- [測試監控策略](https://www.martinfowler.com/articles/testing-observability.html)

## 總結

本監控系統提供：
- ✅ 自動測試執行追蹤
- ✅ AI 品質指標收集
- ✅ 分散式追蹤
- ✅ 即時警報
- ✅ 視覺化儀表板
- ✅ CI/CD 整合

這為測試框架帶來全面的可觀測性，幫助團隊快速識別問題、追蹤品質趨勢，並做出數據驅動的決策。
