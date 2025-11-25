# SuperQuantLab 2.0

一个集成化的加密货币量化研究与展示系统 / An Integrated Crypto Quant Research & Presentation System

## 项目结构 / Project Structure

```
SuperQuantLab 2.0/
├── backend/          # Python FastAPI 后端
├── frontend/         # Next.js 14 前端
├── data/             # 示例数据文件
└── README.md
```

## 快速开始 / Quick Start

### 后端 / Backend

```bash
cd backend
# 使用 uv (推荐)
uv sync
uv run uvicorn app.main:app --reload

# 或使用 poetry
poetry install
poetry run uvicorn app.main:app --reload
```

### 前端 / Frontend

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000

## 功能特性 / Features

- 🚀 核心量化引擎 / Core Quant Engine
- 📊 策略回测与绩效评估 / Backtesting & Performance Evaluation
- 🧠 行为金融分析 / Behavioral Finance Analysis
- 🌊 混沌度分析（Lyapunov指数）/ Chaos Analysis (Lyapunov Exponent)
- 🔬 市场微结构分析 / Market Microstructure Analysis
- 🎯 元策略层 / Meta Strategy Layer
- 🤖 LLM策略生成（占位）/ LLM Strategy Generation (Placeholder)
- 📈 现代化可视化Dashboard / Modern Dashboard

## 技术栈 / Tech Stack

- **Backend**: Python 3.11+, FastAPI, Pydantic
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, shadcn-ui, Recharts
- **Data**: CSV, Binance API (placeholder)

