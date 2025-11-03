# Makefile for SysTalk Chat Test Framework
# 提供常用的開發和測試命令

.PHONY: help install test test-unit test-integration test-e2e test-ai test-llm \
        coverage lint format security clean docker-build docker-test \
        pre-commit ci-local

# 預設目標
.DEFAULT_GOAL := help

# 顏色定義
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## 顯示幫助訊息
	@echo "$(BLUE)SysTalk Chat Test Framework - Available Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# ============================================================================
# 安裝和設置
# ============================================================================

install: ## 安裝所有依賴
	@echo "$(BLUE)📦 Installing dependencies...$(NC)"
	pip install -r requirements.txt
	playwright install chromium
	@echo "$(GREEN)✅ Dependencies installed!$(NC)"

install-dev: ## 安裝開發依賴
	@echo "$(BLUE)📦 Installing dev dependencies...$(NC)"
	pip install -r requirements.txt
	pip install pre-commit black isort flake8 pylint mypy bandit safety
	playwright install chromium
	pre-commit install
	@echo "$(GREEN)✅ Dev dependencies installed!$(NC)"

# ============================================================================
# 測試
# ============================================================================

test: ## 執行所有測試
	@echo "$(BLUE)🧪 Running all tests...$(NC)"
	pytest -v --cov=. --cov-report=html --cov-report=term

test-unit: ## 執行單元測試
	@echo "$(BLUE)🧪 Running unit tests...$(NC)"
	pytest tests/unit/ -v

test-integration: ## 執行整合測試
	@echo "$(BLUE)🧪 Running integration tests...$(NC)"
	pytest tests/integration/ -v

test-e2e: ## 執行 E2E 測試
	@echo "$(BLUE)🧪 Running E2E tests...$(NC)"
	pytest tests/e2e/ -v --html=report.html --self-contained-html

test-ai: ## 執行 AI 品質測試
	@echo "$(BLUE)🤖 Running AI quality tests...$(NC)"
	pytest tests/ai_quality/ -v

test-llm: ## 執行 LLM 特定測試
	@echo "$(BLUE)🤖 Running LLM specific tests...$(NC)"
	pytest tests/llm_specific/ -v

test-smoke: ## 執行煙霧測試
	@echo "$(BLUE)💨 Running smoke tests...$(NC)"
	pytest -m smoke -v

test-quick: ## 快速測試（只執行單元和整合測試）
	@echo "$(BLUE)⚡ Running quick tests...$(NC)"
	pytest tests/unit/ tests/integration/ -v

# ============================================================================
# 覆蓋率
# ============================================================================

coverage: ## 生成覆蓋率報告
	@echo "$(BLUE)📊 Generating coverage report...$(NC)"
	pytest --cov=. --cov-report=html --cov-report=term
	@echo "$(GREEN)✅ Coverage report generated in htmlcov/index.html$(NC)"

coverage-open: coverage ## 生成並打開覆蓋率報告
	@echo "$(BLUE)🌐 Opening coverage report...$(NC)"
	python -m http.server 8000 --directory htmlcov

# ============================================================================
# 程式碼品質
# ============================================================================

lint: ## 執行所有 lint 檢查
	@echo "$(BLUE)🔍 Running linters...$(NC)"
	flake8 .
	pylint **/*.py --exit-zero
	@echo "$(GREEN)✅ Linting completed!$(NC)"

format: ## 格式化程式碼
	@echo "$(BLUE)✨ Formatting code...$(NC)"
	black .
	isort .
	@echo "$(GREEN)✅ Code formatted!$(NC)"

format-check: ## 檢查程式碼格式
	@echo "$(BLUE)🔍 Checking code format...$(NC)"
	black --check --diff .
	isort --check-only --diff .

type-check: ## 執行類型檢查
	@echo "$(BLUE)🔍 Running type checks...$(NC)"
	mypy . --ignore-missing-imports --no-strict-optional

# ============================================================================
# 安全
# ============================================================================

security: ## 執行安全掃描
	@echo "$(BLUE)🔒 Running security scans...$(NC)"
	bandit -r . -f json -o bandit-report.json || true
	bandit -r .
	safety check || true
	@echo "$(GREEN)✅ Security scans completed!$(NC)"

security-report: ## 生成安全報告
	@echo "$(BLUE)📋 Generating security report...$(NC)"
	mkdir -p security-reports
	bandit -r . -f html -o security-reports/bandit-report.html || true
	@echo "$(GREEN)✅ Security report generated in security-reports/$(NC)"

# ============================================================================
# Docker
# ============================================================================

docker-build: ## 構建 Docker 映像
	@echo "$(BLUE)🐳 Building Docker image...$(NC)"
	docker build -t systalk-test-framework:latest .
	@echo "$(GREEN)✅ Docker image built!$(NC)"

docker-test: ## 在 Docker 中執行測試
	@echo "$(BLUE)🐳 Running tests in Docker...$(NC)"
	docker-compose up test-runner

docker-quality: ## 在 Docker 中執行程式碼品質檢查
	@echo "$(BLUE)🐳 Running code quality checks in Docker...$(NC)"
	docker-compose up code-quality

docker-security: ## 在 Docker 中執行安全掃描
	@echo "$(BLUE)🐳 Running security scans in Docker...$(NC)"
	docker-compose up security-scan

docker-clean: ## 清理 Docker 資源
	@echo "$(BLUE)🧹 Cleaning Docker resources...$(NC)"
	docker-compose down -v
	docker system prune -f

# ============================================================================
# CI/CD
# ============================================================================

pre-commit: ## 執行 pre-commit 檢查
	@echo "$(BLUE)🔍 Running pre-commit hooks...$(NC)"
	pre-commit run --all-files

ci-local: ## 模擬 CI pipeline 在本地執行
	@echo "$(BLUE)🚀 Running CI pipeline locally...$(NC)"
	@echo "$(YELLOW)Step 1: Install dependencies$(NC)"
	@$(MAKE) install
	@echo "$(YELLOW)Step 2: Format check$(NC)"
	@$(MAKE) format-check
	@echo "$(YELLOW)Step 3: Lint$(NC)"
	@$(MAKE) lint
	@echo "$(YELLOW)Step 4: Type check$(NC)"
	@$(MAKE) type-check
	@echo "$(YELLOW)Step 5: Security scan$(NC)"
	@$(MAKE) security
	@echo "$(YELLOW)Step 6: Run tests$(NC)"
	@$(MAKE) test
	@echo "$(GREEN)✅ CI pipeline completed successfully!$(NC)"

# ============================================================================
# 清理
# ============================================================================

clean: ## 清理生成的檔案
	@echo "$(BLUE)🧹 Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	rm -rf bandit-report.json
	rm -rf report.html
	@echo "$(GREEN)✅ Cleanup completed!$(NC)"

clean-all: clean docker-clean ## 清理所有生成的檔案和 Docker 資源
	@echo "$(GREEN)✅ All cleanup completed!$(NC)"

# ============================================================================
# 開發工具
# ============================================================================

watch: ## 監視檔案變更並自動執行測試
	@echo "$(BLUE)👀 Watching for changes...$(NC)"
	pytest-watch -- -v

serve-docs: ## 啟動文件伺服器
	@echo "$(BLUE)📚 Starting documentation server...$(NC)"
	@echo "$(GREEN)Documentation available at http://localhost:8000$(NC)"
	python -m http.server 8000 --directory docs

serve-coverage: coverage ## 啟動覆蓋率報告伺服器
	@echo "$(BLUE)📊 Starting coverage report server...$(NC)"
	@echo "$(GREEN)Coverage report available at http://localhost:8001$(NC)"
	python -m http.server 8001 --directory htmlcov

# ============================================================================
# Git 相關
# ============================================================================

git-setup: ## 設定 Git hooks
	@echo "$(BLUE)🔧 Setting up Git hooks...$(NC)"
	pre-commit install
	@echo "$(GREEN)✅ Git hooks installed!$(NC)"

commit: format lint ## 格式化、檢查並準備提交
	@echo "$(GREEN)✅ Ready to commit!$(NC)"
	@echo "$(YELLOW)Run: git add . && git commit$(NC)"

# ============================================================================
# 資料管理
# ============================================================================

data-generate: ## 生成測試資料
	@echo "$(BLUE)📊 Generating test data...$(NC)"
	python utils/test_data_generator.py
	@echo "$(GREEN)✅ Test data generated!$(NC)"

data-validate: ## 驗證測試資料
	@echo "$(BLUE)📋 Validating test data...$(NC)"
	python utils/test_data_validator.py
	@echo "$(GREEN)✅ Test data validated!$(NC)"

data-pipeline: ## 執行完整資料管道
	@echo "$(BLUE)🔄 Running data pipeline...$(NC)"
	dvc repro
	@echo "$(GREEN)✅ Data pipeline completed!$(NC)"

dvc-init: ## 初始化 DVC
	@echo "$(BLUE)🔧 Initializing DVC...$(NC)"
	dvc init
	@echo "$(GREEN)✅ DVC initialized!$(NC)"

dvc-push: ## 推送資料到遠端儲存
	@echo "$(BLUE)⬆️  Pushing data to remote storage...$(NC)"
	dvc push
	@echo "$(GREEN)✅ Data pushed!$(NC)"

dvc-pull: ## 從遠端儲存拉取資料
	@echo "$(BLUE)⬇️  Pulling data from remote storage...$(NC)"
	dvc pull
	@echo "$(GREEN)✅ Data pulled!$(NC)"

dvc-status: ## 檢查 DVC 狀態
	@echo "$(BLUE)📊 Checking DVC status...$(NC)"
	dvc status
