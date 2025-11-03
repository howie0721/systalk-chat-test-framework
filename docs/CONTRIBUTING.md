# 貢獻指南

感謝您對 SysTalk.Chat 測試框架的興趣！我們歡迎所有形式的貢獻。

## 目錄

- [行為準則](#行為準則)
- [開始貢獻](#開始貢獻)
- [開發流程](#開發流程)
- [程式碼風格](#程式碼風格)
- [測試要求](#測試要求)
- [提交規範](#提交規範)
- [Pull Request 流程](#pull-request-流程)
- [問題回報](#問題回報)

## 行為準則

### 我們的承諾

為了營造開放且友善的環境，我們承諾：

- 使用歡迎和包容的語言
- 尊重不同的觀點和經驗
- 優雅地接受建設性批評
- 關注對社群最有利的事情
- 對其他社群成員表現同理心

### 不可接受的行為

- 使用性化的語言或圖像
- 人身攻擊或侮辱性評論
- 公開或私下騷擾
- 未經許可公開他人的私人資訊
- 其他在專業環境中不適當的行為

## 開始貢獻

### 環境設置

1. **Fork 專案**
   ```bash
   # 在 GitHub 上 fork 專案
   # 然後 clone 你的 fork
   git clone https://github.com/YOUR_USERNAME/systalk-chat-test-framework.git
   cd systalk-chat-test-framework
   ```

2. **設置開發環境**
   ```bash
   # 建立虛擬環境
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   
   # 安裝開發依賴
   make install-dev
   
   # 或手動安裝
   pip install -r requirements.txt
   pip install pre-commit black isort flake8 pylint mypy
   
   # 安裝 Git hooks
   pre-commit install
   ```

3. **設置 remote**
   ```bash
   # 添加 upstream
   git remote add upstream https://github.com/ORIGINAL_OWNER/systalk-chat-test-framework.git
   
   # 驗證
   git remote -v
   ```

### 貢獻類型

我們歡迎以下類型的貢獻：

- 🐛 **Bug 修復**: 修復已知的問題
- ✨ **新功能**: 添加新的測試工具或功能
- 📝 **文件**: 改進文件和範例
- 🎨 **程式碼改進**: 重構、優化、程式碼風格
- 🧪 **測試**: 增加測試覆蓋率
- 🔧 **工具**: 改進開發工具和流程

## 開發流程

### 1. 選擇或創建 Issue

- 查看 [Issues](https://github.com/OWNER/REPO/issues) 找到想要解決的問題
- 或創建新的 Issue 描述你想要做的改變
- 在開始工作前，在 Issue 中留言表明你正在處理

### 2. 創建分支

```bash
# 從 main 分支創建新分支
git checkout main
git pull upstream main
git checkout -b feature/your-feature-name

# 分支命名規範:
# - feature/feature-name  (新功能)
# - bugfix/bug-description (Bug 修復)
# - docs/doc-topic (文件更新)
# - refactor/refactor-description (重構)
```

### 3. 開發

```bash
# 進行你的更改
# 記得經常提交
git add .
git commit -m "feat: add new feature"

# 保持與 upstream 同步
git fetch upstream
git rebase upstream/main
```

### 4. 測試

```bash
# 運行所有測試
make test

# 檢查覆蓋率
make coverage

# 執行程式碼品質檢查
make lint

# 執行所有檢查
make check-all
```

### 5. 提交 Pull Request

```bash
# 推送到你的 fork
git push origin feature/your-feature-name

# 然後在 GitHub 上創建 Pull Request
```

## 程式碼風格

### Python 風格

我們遵循 **PEP 8** 風格指南，並使用以下工具：

- **Black**: 程式碼格式化（行長度：127）
- **isort**: import 排序
- **Flake8**: 程式碼檢查
- **Pylint**: 程式碼分析
- **MyPy**: 型別檢查

### 自動格式化

```bash
# 格式化程式碼
make format

# 或手動執行
black . --line-length=127
isort .
```

### 程式碼檢查

```bash
# 執行所有檢查
make lint

# 或個別執行
flake8 .
pylint **/*.py
mypy .
```

### 命名規範

```python
# 類別：PascalCase
class ResponseEvaluator:
    pass

# 函數和變數：snake_case
def evaluate_response():
    test_result = None

# 常數：UPPER_SNAKE_CASE
MAX_RETRY_COUNT = 3

# 私有成員：_開頭
def _internal_method():
    pass
```

### 文件字串

使用 **Google 風格** 的 docstring：

```python
def evaluate(question: str, response: str, context: str = None) -> Dict[str, Any]:
    """
    評估 AI 回應的品質。

    Args:
        question: 使用者的問題
        response: AI 的回應
        context: 可選的上下文資訊

    Returns:
        包含評估結果的字典，包含以下鍵：
        - coherence: 連貫性分數
        - relevance: 相關性分數
        - overall_score: 總分

    Raises:
        ValueError: 當參數無效時

    Example:
        >>> evaluator = ResponseEvaluator()
        >>> result = evaluator.evaluate("問題", "回應")
        >>> print(result["overall_score"])
        0.85
    """
    pass
```

## 測試要求

### 測試覆蓋率

- 新功能必須包含測試
- 目標覆蓋率：**80%+**
- Bug 修復應包含回歸測試

### 測試類型

```python
# 單元測試
def test_function_behavior():
    """測試單個函數的行為"""
    result = function_to_test()
    assert result == expected_value

# 整合測試
def test_component_integration():
    """測試元件間的互動"""
    component_a = ComponentA()
    component_b = ComponentB(component_a)
    assert component_b.works_correctly()

# AI 測試
def test_ai_quality():
    """測試 AI 品質工具"""
    evaluator = ResponseEvaluator()
    result = evaluator.evaluate("question", "response")
    assert result["overall_score"] >= 0.7
```

### 運行測試

```bash
# 運行所有測試
pytest

# 運行特定類型
pytest -m unit
pytest -m integration
pytest -m ai_quality

# 檢查覆蓋率
pytest --cov=. --cov-report=html
```

## 提交規範

我們使用 **Conventional Commits** 規範：

### 提交訊息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 類型

- `feat`: 新功能
- `fix`: Bug 修復
- `docs`: 文件更新
- `style`: 格式調整（不影響程式碼運行）
- `refactor`: 重構
- `perf`: 效能優化
- `test`: 測試相關
- `chore`: 建置流程或輔助工具變動

### 範例

```bash
# 好的提交訊息
git commit -m "feat(ai): add sentiment analysis to response evaluator"
git commit -m "fix(monitoring): resolve metrics collection race condition"
git commit -m "docs: update API documentation for BiasDetector"

# 多行提交訊息
git commit -m "feat(testing): add parallel test execution

- Implement pytest-xdist integration
- Add configuration for optimal worker count
- Update documentation with parallel testing guide

Closes #123"
```

### 提交最佳實踐

1. **保持提交小而專注**
   - 每個提交只做一件事
   - 容易 review 和 revert

2. **寫清楚的訊息**
   - 第一行簡短說明（50字元內）
   - 必要時加上詳細描述
   - 說明「為什麼」而不只是「做了什麼」

3. **經常提交**
   - 完成一個小功能就提交
   - 方便追蹤和除錯

## Pull Request 流程

### 準備 PR

1. **確保所有測試通過**
   ```bash
   make check-all
   ```

2. **更新文件**
   - 更新相關的 README
   - 更新 API 文件
   - 添加使用範例

3. **檢查變更**
   ```bash
   git diff upstream/main
   ```

### 創建 PR

1. 推送到你的 fork
2. 在 GitHub 上創建 Pull Request
3. 填寫 PR 模板

### PR 描述模板

```markdown
## 描述
簡短描述這個 PR 做了什麼。

## 相關 Issue
Closes #123

## 變更類型
- [ ] Bug 修復
- [ ] 新功能
- [ ] 重大變更
- [ ] 文件更新

## 變更清單
- 添加了 X 功能
- 修復了 Y 問題
- 更新了 Z 文件

## 測試
- [ ] 添加了新的測試
- [ ] 所有測試通過
- [ ] 覆蓋率 >= 80%

## 檢查清單
- [ ] 程式碼遵循專案風格
- [ ] 包含適當的測試
- [ ] 更新了相關文件
- [ ] 所有 CI 檢查通過

## 截圖（如適用）

## 額外備註
```

### Review 流程

1. **維護者 review**
   - 檢查程式碼品質
   - 測試覆蓋率
   - 文件完整性

2. **CI 檢查**
   - 所有測試必須通過
   - 程式碼品質檢查通過
   - 無安全漏洞

3. **討論和修改**
   - 回應 review 意見
   - 進行必要的修改
   - 推送更新

4. **合併**
   - 獲得批准後
   - 維護者合併 PR
   - 自動部署（如適用）

### 回應 Review

```bash
# 進行修改後
git add .
git commit -m "refactor: address review comments"
git push origin feature/your-feature-name

# PR 會自動更新
```

## 問題回報

### Bug 報告

使用 Issue 模板報告 Bug：

```markdown
**描述 Bug**
清楚簡潔地描述 bug。

**重現步驟**
1. 執行 '...'
2. 點擊 '....'
3. 捲動到 '....'
4. 看到錯誤

**預期行為**
清楚簡潔地描述你預期發生什麼。

**實際行為**
描述實際發生了什麼。

**截圖**
如適用，添加截圖幫助解釋問題。

**環境**
- OS: [e.g. Windows 11]
- Python 版本: [e.g. 3.12.2]
- 框架版本: [e.g. 1.0.0]

**額外資訊**
其他相關的上下文資訊。
```

### 功能請求

```markdown
**功能描述**
清楚簡潔地描述你想要的功能。

**問題**
這個功能解決什麼問題？

**建議的解決方案**
描述你希望如何實作。

**替代方案**
描述你考慮過的其他方案。

**額外資訊**
其他相關的上下文或截圖。
```

## 社群

### 溝通管道

- **GitHub Issues**: Bug 報告和功能請求
- **GitHub Discussions**: 一般討論和問題
- **Pull Requests**: 程式碼 review 和討論

### 獲得幫助

- 查看 [文件](../README.md)
- 搜尋現有的 Issues
- 創建新的 Discussion

### 成為維護者

積極貢獻者可能被邀請成為維護者：

- 持續高品質的貢獻
- 幫助 review PR
- 協助社群成員
- 改進文件和流程

## 開發工具

### 有用的命令

```bash
# 格式化程式碼
make format

# 檢查程式碼品質
make lint

# 執行測試
make test

# 生成覆蓋率報告
make coverage

# 執行所有檢查
make check-all

# 清理生成的檔案
make clean
```

### Pre-commit Hooks

自動在提交前執行檢查：

```bash
# 安裝 hooks
pre-commit install

# 手動執行
pre-commit run --all-files
```

### IDE 設定

#### VS Code

建議的 `.vscode/settings.json`:

```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length=127"],
  "editor.formatOnSave": true,
  "python.testing.pytestEnabled": true
}
```

#### PyCharm

1. Settings → Tools → Black → Enable on save
2. Settings → Tools → Pylint → Enable
3. Settings → Testing → Default test runner → pytest

## 授權

貢獻到此專案，即表示您同意您的貢獻將使用與專案相同的 MIT 授權。

## 感謝

感謝所有貢獻者讓這個專案變得更好！

### 貢獻者名單

查看 [Contributors](https://github.com/OWNER/REPO/graphs/contributors) 頁面。

## 問題？

如有任何問題，請：

1. 查看 [FAQ](../README.md#faq)
2. 搜尋現有 Issues
3. 創建新的 Discussion
4. 聯繫維護者

---

再次感謝您的貢獻！🎉
