# SuperQuantLab 2.0 / SuperQuantLab 2.0

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个集成化的加密货币量化研究与展示系统 / An Integrated Crypto Quant Research & Presentation System

---

## 📖 项目简介 / Project Introduction

**中文：**

SuperQuantLab 2.0 是一个全栈量化交易研究平台，集成了核心量化引擎、行为金融分析、混沌度分析（Lyapunov指数）、市场微结构分析和元策略层。系统提供现代化的 Web Dashboard，支持策略回测、绩效评估、风险指标分析，以及通过 LLM 自然语言生成策略配置。

**English:**

SuperQuantLab 2.0 is a full-stack quant trading research platform that integrates core quant engines, behavioral finance analysis, chaos analysis (Lyapunov exponent), market microstructure analysis, and meta-strategy layers. The system provides a modern Web Dashboard supporting strategy backtesting, performance evaluation, risk metrics analysis, and LLM-based natural language strategy generation.

---

## ✨ 核心功能 / Core Features

### 🚀 量化引擎 / Quant Engine
- **策略系统** / Strategy System: 支持自定义策略（均线交叉、均线密集开仓法等）
- **回测引擎** / Backtest Engine: 单/多策略回测，支持手续费、滑点模拟
- **绩效评估** / Performance Metrics: 年化收益、夏普比率、最大回撤、胜率等

### 🧠 行为金融分析 / Behavioral Finance Analysis
- **冲动指数** / Impulsiveness Index: 基于操作间隔的行为冲动度分析
- **追涨杀跌指数** / Chase-Selloff Index: 追高和恐慌性抛售行为统计
- **连续亏损检测** / Consecutive Loss Detection: 交易行为模式识别

### 🌊 混沌度分析 / Chaos Analysis
- **Lyapunov 指数** / Lyapunov Exponent: 市场混沌度近似计算
- **混沌指数** / Chaos Index: 0-1 范围的混沌度指标
- **市场状态分类** / Regime Classification: TREND / NEUTRAL / CHAOTIC

### 🔬 市场微结构分析 / Market Microstructure Analysis
- **鲸鱼活动指数** / Whale Activity Index: 大额交易活动分析
- **杠杆风险指数** / Leverage Risk Index: 基于OI和波动率的风险评估

### 🎯 元策略层 / Meta Strategy Layer
- **动态仓位调整** / Dynamic Position Sizing: 基于市场状态的仓位倍数
- **交易开关决策** / Trading Gate: 综合多引擎指标的交易许可控制

### 🤖 LLM 策略生成 / LLM Strategy Generation
- **自然语言生成策略** / Natural Language to Strategy: 将自然语言描述转换为策略配置（占位实现）

### 📈 现代化 Dashboard / Modern Dashboard
- **暗色主题 UI** / Dark Theme UI: 使用 Tailwind CSS + shadcn-ui
- **中英双语支持** / Bilingual Support: 完整的中英文界面
- **实时图表** / Real-time Charts: 权益曲线、回撤、混沌指数、市场状态时间轴

---

## 🏗️ 项目结构 / Project Structure

```
SuperQuantLab-2.0/
├── backend/                 # Python FastAPI 后端 / Backend
│   ├── app/
│   │   ├── main.py         # FastAPI 应用入口 / Entry point
│   │   ├── core/           # 配置管理 / Configuration
│   │   ├── models/         # 数据模型 / Data models
│   │   ├── data/           # 数据加载与转换 / Data loading & transforms
│   │   ├── strategies/     # 策略实现 / Strategies
│   │   ├── engines/        # 引擎模块 / Engines
│   │   ├── services/       # 服务层 / Services
│   │   ├── api/            # API 路由 / API routes
│   │   └── tests/          # 测试 / Tests
│   ├── pyproject.toml      # Poetry 配置 / Poetry config
│   └── README.md           # 后端文档 / Backend docs
├── frontend/               # Next.js 14 前端 / Frontend
│   ├── app/                # 页面路由 / Pages
│   ├── components/         # React 组件 / Components
│   ├── lib/                # 工具库 / Utilities
│   └── package.json        # NPM 配置 / NPM config
├── data/                   # 数据文件目录 / Data directory
│   ├── *.csv               # OHLCV 数据文件 / OHLCV data files
│   └── README.md           # 数据格式说明 / Data format docs
├── README.md               # 项目总览 / Project overview
├── PROJECT_SUMMARY.md      # 详细功能说明 / Detailed features
├── START_GUIDE.md          # 启动指南 / Startup guide
└── GITHUB_SETUP.md         # GitHub 设置说明 / GitHub setup guide
```

---

## 🚀 快速开始 / Quick Start

### 前置要求 / Prerequisites

- **Python 3.11+** 
- **Node.js 18+**
- **Poetry** 或 **uv** (Python 包管理)
- **npm** 或 **yarn** (Node.js 包管理)

### 1️⃣ 克隆仓库 / Clone Repository

```bash
git clone https://github.com/ninglinLiu/SuperQuantLab-2.0.git
cd SuperQuantLab-2.0
```

### 2️⃣ 后端设置 / Backend Setup

```bash
cd backend

# 使用 Poetry (推荐 / Recommended)
poetry install
poetry run uvicorn app.main:app --reload

# 或使用 uv
uv sync
uv run uvicorn app.main:app --reload
```

后端将在 http://localhost:8000 启动  
API 文档: http://localhost:8000/docs

**Backend starts at http://localhost:8000**  
**API Docs: http://localhost:8000/docs**

### 3️⃣ 前端设置 / Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

前端将在 http://localhost:3000 启动

**Frontend starts at http://localhost:3000**

### 4️⃣ 数据准备 / Data Preparation

将 OHLCV 数据文件放到 `data/` 目录：

**Place OHLCV data files in `data/` directory:**

- 文件命名格式 / File naming: `{SYMBOL}_{TIMEFRAME}.csv`
- 示例 / Example: `BTCUSDT_1h.csv`
- CSV 格式要求 / CSV format:
  ```csv
  timestamp,open,high,low,close,volume
  2024-01-01T00:00:00,42000.0,42500.0,41800.0,42300.0,1234.56
  ```

**注意 / Note:** 系统已配置演示数据，即使没有真实数据文件也能正常展示所有功能。

**The system is configured with demo data, so all features will work even without real data files.**

---

## 📚 功能详解 / Features Details

### 策略系统 / Strategy System

系统实现了两种示例策略：

**The system implements two example strategies:**

1. **MA Crossover** / **均线交叉策略**
   - 短期/长期均线交叉信号
   - 可配置参数：短期窗口、长期窗口、仓位大小
   - **Short/long MA crossover signals**
   - **Configurable: short window, long window, position size**

2. **MA Cluster Density** / **均线密集开仓法**
   - 多个均线密集排列时开仓
   - 突破确认后进入市场
   - **Entry when multiple MAs cluster together**
   - **Market entry after breakout confirmation**

### API 端点 / API Endpoints

- `POST /api/v1/backtest/run` - 运行回测 / Run backtest
- `GET /api/v1/strategies` - 列出策略 / List strategies
- `POST /api/v1/strategies/from-llm` - LLM生成策略 / Generate strategy with LLM
- `GET /api/v1/metrics/chaos` - 混沌指标 / Chaos metrics
- `GET /api/v1/metrics/behavior` - 行为指标 / Behavior metrics
- `GET /api/v1/metrics/regime` - 市场状态 / Market regime

完整 API 文档可在 http://localhost:8000/docs 查看

**Full API documentation available at http://localhost:8000/docs**

---

## 🛠️ 技术栈 / Tech Stack

### 后端 / Backend
- **Python 3.11+**
- **FastAPI** - 现代 Python Web 框架
- **Pydantic** - 数据验证
- **NumPy & Pandas** - 数值计算与数据处理

### 前端 / Frontend
- **Next.js 14** - React 框架
- **TypeScript** - 类型安全
- **Tailwind CSS** - 样式框架
- **shadcn-ui** - UI 组件库
- **Recharts** - 图表可视化

---

## 📖 文档 / Documentation

- [项目总结 / Project Summary](PROJECT_SUMMARY.md) - 详细功能说明
- [启动指南 / Startup Guide](START_GUIDE.md) - 快速启动教程
- [GitHub 设置 / GitHub Setup](GITHUB_SETUP.md) - 仓库设置说明
- [后端文档 / Backend Docs](backend/README.md) - 后端详细文档
- [前端文档 / Frontend Docs](frontend/README.md) - 前端详细文档
- [数据格式 / Data Format](data/README.md) - 数据文件格式说明

---

## 🔮 待完成功能 / TODO

以下功能已预留接口，待进一步实现：

**The following features have interfaces prepared for future implementation:**

- [ ] 真实交易所 API 集成（Binance/OKX）
- [ ] LLM API 真实集成（OpenAI/DeepSeek）
- [ ] 数据库集成（策略配置持久化）
- [ ] 更多策略模板（RSI、MACD、布林带等）
- [ ] 多品种组合回测
- [ ] 参数优化功能
- [ ] 实时交易（模拟/实盘）

**English:**
- [ ] Real exchange API integration (Binance/OKX)
- [ ] Real LLM API integration (OpenAI/DeepSeek)
- [ ] Database integration (strategy persistence)
- [ ] More strategy templates (RSI, MACD, Bollinger Bands, etc.)
- [ ] Multi-asset portfolio backtesting
- [ ] Parameter optimization
- [ ] Live trading (simulated/real)

---

## 🤝 贡献 / Contributing

欢迎提交 Issue 和 Pull Request！

**Contributions are welcome! Please feel free to submit Issues and Pull Requests.**

---

## 📝 许可证 / License

本项目为示例/教学用途。

**This project is for educational/demonstration purposes.**

---

## 👤 作者 / Author

**ninglinLiu**

GitHub: [@ninglinLiu](https://github.com/ninglinLiu)

---

## 🙏 致谢 / Acknowledgments

- FastAPI 团队
- Next.js 团队
- shadcn/ui 社区
- 所有开源贡献者

**English:**
- FastAPI Team
- Next.js Team
- shadcn/ui Community
- All open-source contributors

---

## 📊 项目状态 / Project Status

✅ 核心功能完成 / Core features completed  
✅ 演示数据已配置 / Demo data configured  
✅ API 文档完整 / API documentation complete  
✅ 前端界面完成 / Frontend UI complete  
🚧 LLM 集成待完善 / LLM integration pending  
🚧 真实交易所 API 待集成 / Real exchange API pending

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**

**⭐ If this project helps you, please give it a Star!**
