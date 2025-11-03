# CI/CD Pipeline 文檔

## 概述

本專案使用 GitHub Actions 建立完整的 CI/CD pipeline，確保程式碼品質、安全性和自動化測試。

## Pipeline 架構

### 1. 主要 CI Pipeline (`.github/workflows/ci.yml`)

觸發條件：
- Push 到 `master`, `main`, `develop` 分支
- Pull Request 到 `master`, `main`, `develop` 分支
- 手動觸發

#### Jobs:

**Test Suite** (`test`)
- 多平台測試：Ubuntu + Windows
- 多版本測試：Python 3.10, 3.11, 3.12
- 測試類型：
  - Unit tests（單元測試）
  - Integration tests（整合測試）
  - AI quality tests（AI 品質測試）
  - LLM specific tests（LLM 特定測試）
- 自動上傳覆蓋率報告到 Codecov

**Code Quality Checks** (`code-quality`)
- Black：程式碼格式化檢查
- isort：import 排序檢查
- Flake8：程式碼風格檢查
- Pylint：程式碼品質檢查
- MyPy：靜態類型檢查
- Bandit：安全漏洞掃描
- Safety：依賴漏洞檢查

**E2E Tests** (`e2e-tests`)
- Playwright 瀏覽器測試
- 生成 HTML 測試報告
- 自動上傳測試報告

**Coverage Report** (`coverage-report`)
- 生成完整的覆蓋率報告
- 在 PR 上自動評論覆蓋率變化

**Build Documentation** (`build-docs`)
- 構建專案文檔
- 驗證文檔完整性

### 2. Nightly Build (`.github/workflows/nightly.yml`)

觸發條件：
- 每天凌晨 2:00 UTC 自動執行
- 手動觸發

#### Jobs:

**Nightly Full Test Suite**
- 完整測試套件執行
- 生成詳細測試報告
- 保留 7 天的測試結果

**Performance Testing**
- 使用 pytest-benchmark 進行性能測試
- 追蹤性能變化趨勢
- 生成基準測試報告

**Dependency Check**
- 檢查過時的套件
- 依賴安全性審計
- 生成依賴報告

### 3. Release Pipeline (`.github/workflows/release.yml`)

觸發條件：
- Push tag 格式 `v*.*.*`（如 v1.0.0）
- 手動觸發並指定版本

#### Jobs:

**Validate Release**
- 完整測試套件
- 程式碼品質檢查
- 安全掃描
- 版本號驗證

**Build Package**
- 構建 Python package
- 驗證 package 完整性
- 上傳構建產物

**Create GitHub Release**
- 自動生成 changelog
- 創建 GitHub Release
- 附加構建產物

**Docker Release**
- 構建 Docker 映像
- Tag 管理（version, major.minor, major）
- 推送到 Docker Hub（可選）

## 本地開發工具

### Makefile 指令

```bash
# 查看所有可用指令
make help

# 安裝依賴
make install          # 基本依賴
make install-dev      # 開發依賴 + pre-commit hooks

# 執行測試
make test             # 所有測試
make test-unit        # 單元測試
make test-integration # 整合測試
make test-ai          # AI 測試
make test-llm         # LLM 測試
make test-quick       # 快速測試（單元+整合）

# 覆蓋率
make coverage         # 生成覆蓋率報告
make coverage-open    # 生成並打開報告

# 程式碼品質
make lint             # 執行 linters
make format           # 格式化程式碼
make format-check     # 檢查格式
make type-check       # 類型檢查

# 安全
make security         # 安全掃描
make security-report  # 生成安全報告

# Docker
make docker-build     # 構建 Docker 映像
make docker-test      # 在 Docker 中測試
make docker-quality   # Docker 中程式碼品質檢查
make docker-security  # Docker 中安全掃描

# CI/CD
make pre-commit       # 執行 pre-commit hooks
make ci-local         # 本地模擬 CI pipeline

# 清理
make clean            # 清理生成檔案
make clean-all        # 清理所有（包括 Docker）
```

### Docker Compose

```bash
# 執行所有測試
docker-compose up test-runner

# 程式碼品質檢查
docker-compose up code-quality

# 安全掃描
docker-compose up security-scan

# 清理
docker-compose down -v
```

### Pre-commit Hooks

安裝 pre-commit hooks：
```bash
make install-dev
# 或
pre-commit install
```

手動執行所有 hooks：
```bash
make pre-commit
# 或
pre-commit run --all-files
```

配置的 hooks：
- Black（程式碼格式化）
- isort（import 排序）
- Flake8（風格檢查）
- Trailing whitespace
- End of file fixer
- YAML/JSON/TOML 檢查
- Large files 檢查
- Merge conflict 檢查
- Debug statements 檢查
- Bandit（安全檢查）
- MyPy（類型檢查）

## 配置文件說明

### `.flake8`
- 程式碼風格配置
- 最大行長度：127
- 排除目錄和忽略的錯誤

### `.pylintrc`
- 更嚴格的程式碼品質檢查
- 設計規則（參數數量、複雜度等）
- 相似度檢查

### `mypy.ini`
- 靜態類型檢查配置
- 逐步啟用嚴格模式
- 測試檔案較寬鬆的規則

### `.bandit`
- 安全問題檢查配置
- 排除測試目錄
- 嚴重性和信心等級設定

### `.pre-commit-config.yaml`
- Git pre-commit hooks 配置
- 自動化程式碼品質檢查
- 防止不符合標準的程式碼被提交

## CI/CD 最佳實踐

### 1. 快速失敗原則
- 先執行快速的檢查（格式化、linting）
- 再執行較慢的測試
- 盡早發現問題

### 2. 並行執行
- 獨立的 jobs 並行執行
- 多版本測試並行
- 縮短總執行時間

### 3. 快取策略
- pip 依賴快取
- Docker layer 快取
- 加速 CI 執行

### 4. 測試分類
- 按測試類型分別執行
- 便於定位問題
- 生成分類報告

### 5. 產物保留
- 測試報告保留 30 天
- 覆蓋率報告上傳
- 便於歷史追蹤

## 整合服務

### Codecov
- 覆蓋率追蹤和視覺化
- PR 上自動評論
- 覆蓋率趨勢分析

設定：需要在 GitHub Secrets 中設定 `CODECOV_TOKEN`

### Docker Hub（可選）
- Docker 映像發布
- 版本管理

設定：需要設定 `DOCKER_USERNAME` 和 `DOCKER_PASSWORD`

## 故障排除

### CI 失敗常見原因

1. **測試失敗**
   - 檢查測試日誌
   - 本地重現問題：`make test`

2. **格式化問題**
   - 執行：`make format`
   - 提交更改

3. **Linting 錯誤**
   - 檢查具體錯誤訊息
   - 修正或配置忽略

4. **依賴問題**
   - 確認 `requirements.txt` 正確
   - 檢查版本衝突

5. **Playwright 瀏覽器問題**
   - 確認瀏覽器已安裝
   - 檢查系統依賴

## 本地模擬 CI

完整模擬 CI pipeline：
```bash
make ci-local
```

這將執行：
1. 安裝依賴
2. 格式檢查
3. Linting
4. 類型檢查
5. 安全掃描
6. 所有測試

## 效能優化建議

1. **減少測試矩陣組合**
   - 目前：6 組合（2 OS × 3 Python 版本，排除 2 組）
   - 可根據需求調整

2. **使用 pytest-xdist 並行測試**
   ```bash
   pytest -n auto
   ```

3. **選擇性執行測試**
   - 只測試變更的檔案
   - 使用 pytest markers

4. **優化 Docker 映像**
   - 多階段構建
   - 減少 layer 數量

## 監控和報告

### 可用報告
- 測試報告（HTML）
- 覆蓋率報告（HTML）
- 安全報告（JSON/HTML）
- 基準測試報告（JSON）

### 訪問報告
在 GitHub Actions 的 Artifacts 中下載，或在 PR 中查看自動評論。

## 後續改進

1. ☐ 整合 Allure 報告
2. ☐ 添加性能回歸測試
3. ☐ 整合 SonarQube
4. ☐ 添加自動化回滾機制
5. ☐ 整合通知服務（Slack/Email）
6. ☐ 添加部署 stages
