# API 測試工具使用指南

> 符合 TPIsoftware QA JD 要求：Postman、JMeter、自動化測試

## 📋 工具概覽

根據你的職位需求，我們整合了以下 API 測試工具：

### 1️⃣ **Postman** - API 功能測試
- **用途**：API 功能測試、手動探索性測試
- **整合方式**：匯出 Postman Collection → 轉換為 pytest 測試

### 2️⃣ **JMeter** - 效能/壓力測試  
- **用途**：效能測試、壓力測試、負載測試
- **整合方式**：JMeter GUI 設計測試計劃 → 命令列執行 → 報告整合

### 3️⃣ **Locust** - Python 效能測試（JMeter 替代方案）
- **用途**：效能測試、壓力測試（可完全用 Python 撰寫）
- **優勢**：與 pytest 生態系統完美整合

---

## 🎯 Postman 整合方案

### Postman Collection 轉 pytest 自動化

**流程：**
```
Postman Collection (手動測試)
    ↓
匯出 JSON
    ↓
pytest 自動化測試
    ↓
CI/CD 整合
```

### 範例結構

**Postman Collection 範例：**
```json
{
  "info": {
    "name": "SysTalk.Chat API Tests",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Chat Message",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/api/chat/message",
        "body": {
          "mode": "raw",
          "raw": "{\n  \"user_id\": \"test_user_001\",\n  \"message\": \"查詢帳戶餘額\"\n}"
        }
      },
      "response": []
    }
  ]
}
```

**轉換為 pytest 測試：**
```python
# tests/integration/test_chat_api.py
import pytest
import requests


class TestChatAPI:
    """聊天 API 測試（來自 Postman Collection）"""
    
    @pytest.fixture
    def base_url(self, config):
        return config["api_url"]
    
    def test_send_chat_message(self, base_url):
        """測試發送聊天訊息 (Postman: Chat Message)"""
        # 對應 Postman 的 Request
        response = requests.post(
            f"{base_url}/api/chat/message",
            json={
                "user_id": "test_user_001",
                "message": "查詢帳戶餘額"
            }
        )
        
        # 對應 Postman 的 Tests
        assert response.status_code == 200
        assert "intent" in response.json()
        assert response.json()["intent"] == "account_inquiry"
```

---

## 🚀 JMeter 整合方案

### 方案 A：直接使用 JMeter（傳統方式）

**1. 安裝 JMeter**
```powershell
# 使用 Chocolatey 安裝
choco install jmeter

# 或手動下載
# https://jmeter.apache.org/download_jmeter.cgi
```

**2. JMeter 測試計劃結構**
```
SysTalk_Chat_Load_Test.jmx
├── Thread Group (使用者群組)
│   ├── HTTP Request: Login
│   ├── HTTP Request: Send Message
│   └── HTTP Request: Get Response
├── Listeners (監聽器)
│   ├── View Results Tree
│   ├── Summary Report
│   └── Response Time Graph
└── Assertions (斷言)
    ├── Response Assertion
    └── Duration Assertion
```

**3. JMeter 命令列執行**
```powershell
# 在專案目錄下
jmeter -n -t tests/performance/jmeter/SysTalk_Chat_Load_Test.jmx `
       -l reports/jmeter/results.jtl `
       -e -o reports/jmeter/html
```

**4. 整合到 pytest**
```python
# tests/performance/test_jmeter_integration.py
import pytest
import subprocess
import os
from pathlib import Path


class TestJMeterPerformance:
    """JMeter 效能測試整合"""
    
    @pytest.mark.performance
    def test_chat_load_test(self, project_root, reports_dir):
        """執行 JMeter 聊天負載測試"""
        jmx_file = project_root / "tests/performance/jmeter/SysTalk_Chat_Load_Test.jmx"
        results_file = reports_dir / "jmeter/results.jtl"
        html_report = reports_dir / "jmeter/html"
        
        # 執行 JMeter
        cmd = [
            "jmeter",
            "-n",  # 非 GUI 模式
            "-t", str(jmx_file),  # 測試計劃
            "-l", str(results_file),  # 結果文件
            "-e",  # 生成報告
            "-o", str(html_report)  # HTML 報告目錄
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # 驗證執行成功
        assert result.returncode == 0, f"JMeter 執行失敗: {result.stderr}"
        assert results_file.exists(), "結果文件未生成"
        
        # 解析結果並驗證效能指標
        self._validate_performance_metrics(results_file)
    
    def _validate_performance_metrics(self, results_file):
        """驗證效能指標"""
        # 解析 JTL 結果文件
        import pandas as pd
        df = pd.read_csv(results_file)
        
        # 計算指標
        avg_response_time = df['elapsed'].mean()
        p95_response_time = df['elapsed'].quantile(0.95)
        error_rate = (df['success'] == False).sum() / len(df)
        
        # 斷言效能需求
        assert avg_response_time < 1000, f"平均響應時間過長: {avg_response_time}ms"
        assert p95_response_time < 2000, f"P95 響應時間過長: {p95_response_time}ms"
        assert error_rate < 0.01, f"錯誤率過高: {error_rate*100}%"
```

---

### 方案 B：使用 Locust（Python 原生，推薦！）

**為什麼選擇 Locust？**
- ✅ 純 Python 撰寫，與 pytest 無縫整合
- ✅ 程式碼即測試計劃，易於版本控制
- ✅ 即時 Web UI 監控
- ✅ 分散式負載測試支援

**1. 創建 Locust 測試腳本**
```python
# tests/performance/locustfile.py
from locust import HttpUser, task, between
import random


class SysTalkChatUser(HttpUser):
    """模擬 SysTalk.Chat 使用者行為"""
    
    wait_time = between(1, 3)  # 使用者操作間隔 1-3 秒
    
    def on_start(self):
        """測試開始時執行（模擬登入）"""
        self.client.post("/api/auth/login", json={
            "user_id": f"test_user_{random.randint(1000, 9999)}",
            "session_id": self.generate_session_id()
        })
    
    @task(3)  # 權重 3：最常見的操作
    def send_message(self):
        """發送聊天訊息"""
        messages = [
            "查詢帳戶餘額",
            "申請信用卡",
            "投訴服務",
            "轉接人工客服",
            "查詢交易記錄"
        ]
        
        self.client.post("/api/chat/message", json={
            "message": random.choice(messages),
            "timestamp": self.get_timestamp()
        }, name="/api/chat/message")
    
    @task(1)  # 權重 1：較少的操作
    def get_history(self):
        """取得歷史訊息"""
        self.client.get("/api/chat/history", name="/api/chat/history")
    
    @task(2)
    def feedback(self):
        """提供回饋"""
        self.client.post("/api/chat/feedback", json={
            "rating": random.randint(1, 5),
            "comment": "測試回饋"
        }, name="/api/chat/feedback")
    
    def generate_session_id(self):
        import uuid
        return str(uuid.uuid4())
    
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()
```

**2. 執行 Locust 測試**

**方式 1：Web UI 模式（推薦用於測試設計）**
```powershell
# 啟動 Locust Web UI
cd tests/performance
locust -f locustfile.py --host=http://localhost:3000

# 開啟瀏覽器訪問 http://localhost:8089
# 設定使用者數量、增長速率，開始測試
```

**方式 2：命令列模式（用於 CI/CD）**
```powershell
# 無頭模式執行
locust -f tests/performance/locustfile.py `
       --host=http://localhost:3000 `
       --users 100 `
       --spawn-rate 10 `
       --run-time 5m `
       --headless `
       --html reports/locust/report.html `
       --csv reports/locust/stats
```

**3. 整合到 pytest**
```python
# tests/performance/test_locust_integration.py
import pytest
import subprocess
from pathlib import Path


class TestLocustPerformance:
    """Locust 效能測試整合"""
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_chat_performance_100_users(self, project_root, reports_dir):
        """測試 100 個並發使用者的效能"""
        locustfile = project_root / "tests/performance/locustfile.py"
        html_report = reports_dir / "locust/report.html"
        csv_prefix = reports_dir / "locust/stats"
        
        cmd = [
            "locust",
            "-f", str(locustfile),
            "--host", "http://localhost:3000",
            "--users", "100",
            "--spawn-rate", "10",
            "--run-time", "2m",
            "--headless",
            "--html", str(html_report),
            "--csv", str(csv_prefix)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        assert result.returncode == 0, f"Locust 執行失敗: {result.stderr}"
        assert html_report.exists(), "報告未生成"
        
        # 驗證效能指標
        self._validate_locust_results(csv_prefix)
    
    def _validate_locust_results(self, csv_prefix):
        """驗證 Locust 測試結果"""
        import pandas as pd
        
        # 讀取統計結果
        stats_file = Path(f"{csv_prefix}_stats.csv")
        df = pd.read_csv(stats_file)
        
        # 過濾掉 "Aggregated" 行
        df = df[df['Type'] != 'Aggregated']
        
        # 驗證所有 API 的效能
        for _, row in df.iterrows():
            assert row['Failure Count'] == 0, f"{row['Name']} 有 {row['Failure Count']} 個失敗"
            assert row['Average Response Time'] < 1000, \
                f"{row['Name']} 平均響應時間過長: {row['Average Response Time']}ms"
```

---

## 📊 測試計劃對比

| 特性 | Postman | JMeter | Locust |
|------|---------|--------|--------|
| **主要用途** | API 功能測試 | 效能/壓力測試 | 效能/壓力測試 |
| **學習曲線** | ⭐ 簡單 | ⭐⭐⭐ 中等 | ⭐⭐ 簡單 |
| **腳本語言** | JavaScript | XML/GUI | Python |
| **CI/CD 整合** | ✅ 容易 | ✅ 可以 | ✅ 非常容易 |
| **即時監控** | ❌ 無 | ✅ 有（外掛） | ✅ Web UI |
| **分散式測試** | ❌ 無 | ✅ 支援 | ✅ 支援 |
| **與 Python 整合** | ⭐⭐ 中等 | ⭐⭐ 中等 | ⭐⭐⭐ 完美 |

---

## 🎯 建議的測試策略

### 1. **功能測試**（每次 Commit）
- 使用 **pytest + requests**
- 從 Postman Collection 轉換而來
- 快速、穩定、易維護

### 2. **整合測試**（每日/每週）
- 使用 **pytest + 真實環境**
- 驗證完整業務流程

### 3. **效能測試**（發布前）
- 使用 **Locust**（推薦）或 **JMeter**
- 模擬真實負載
- 生成效能報告

### 4. **壓力測試**（重大發布前）
- 使用 **JMeter** 或 **Locust**
- 找出系統瓶頸
- 驗證系統穩定性

---

## 📁 專案目錄結構

```
systalk-chat-test-framework/
├── tests/
│   ├── integration/
│   │   ├── test_chat_api.py          # 從 Postman 轉換
│   │   └── test_auth_api.py
│   ├── performance/
│   │   ├── locustfile.py             # Locust 腳本
│   │   ├── test_locust_integration.py
│   │   ├── jmeter/
│   │   │   └── SysTalk_Chat_Load_Test.jmx  # JMeter 測試計劃
│   │   └── test_jmeter_integration.py
│   └── postman/
│       ├── collections/
│       │   └── SysTalk_Chat_API.postman_collection.json
│       └── environments/
│           └── dev.postman_environment.json
├── docs/
│   └── API_Testing_Tools_Guide.md    # 本文件
└── reports/
    ├── postman/
    ├── jmeter/
    │   ├── results.jtl
    │   └── html/
    └── locust/
        ├── report.html
        └── stats_*.csv
```

---

## 🚀 快速開始

### 安裝依賴
```powershell
# 啟動虛擬環境
.\venv\Scripts\Activate.ps1

# 安裝所有測試工具
pip install -r requirements.txt

# 安裝 JMeter (可選)
choco install jmeter
```

### 執行測試
```powershell
# 1. API 功能測試 (Postman 轉換)
pytest tests/integration/ -v

# 2. 效能測試 (Locust)
locust -f tests/performance/locustfile.py --host=http://localhost:3000

# 3. 效能測試 (JMeter - 如果已安裝)
pytest tests/performance/test_jmeter_integration.py -v

# 4. 完整測試套件
pytest --cov=. --html=reports/pytest/report.html
```

---

## 💡 面試重點展示

在展示這個專案時，重點說明：

1. **Postman 經驗**
   - "我使用 Postman 進行 API 探索性測試和手動驗證"
   - "將 Postman Collection 轉換為自動化 pytest 測試"
   - "確保手動測試和自動化測試的一致性"

2. **JMeter 經驗**
   - "使用 JMeter 進行壓力測試和效能基準測試"
   - "設計測試計劃模擬真實使用者行為"
   - "整合 JMeter 到 CI/CD Pipeline"

3. **自動化測試**
   - "使用 pytest 建立完整的自動化測試框架"
   - "整合多種測試工具（Postman、JMeter、Locust）"
   - "實現持續測試和持續整合"

---

## 📚 延伸學習資源

- **Postman Learning Center**: https://learning.postman.com/
- **JMeter 教學**: https://jmeter.apache.org/usermanual/
- **Locust 文件**: https://docs.locust.io/
- **API 測試最佳實踐**: https://www.postman.com/api-testing-best-practices/

---

**🎓 記住：工具只是手段，重要的是測試思維和策略！**
