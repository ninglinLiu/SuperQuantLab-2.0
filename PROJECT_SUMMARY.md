# SuperQuantLab 2.0 项目总结 / Project Summary

## 项目概述 / Overview

SuperQuantLab 2.0 是一个完整的加密货币量化交易研究与展示系统，包含：

1. **核心量化引擎** - 支持策略回测、绩效评估、风险指标
2. **高级分析模块** - 行为引擎、混沌引擎、微结构引擎、元策略层
3. **LLM策略生成** - 通过自然语言生成策略配置（占位实现）
4. **现代化前端** - Next.js 14 + TypeScript + Tailwind + shadcn-ui + Recharts

## 技术栈 / Tech Stack

### 后端 / Backend
- Python 3.11+
- FastAPI
- Pydantic
- NumPy, Pandas

### 前端 / Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- shadcn-ui
- Recharts

## 项目结构 / Project Structure

```
SuperQuantLab 2.0/
├── backend/              # Python FastAPI 后端
│   ├── app/
│   │   ├── main.py      # FastAPI 入口
│   │   ├── core/        # 配置管理
│   │   ├── models/      # 数据模型
│   │   ├── data/        # 数据加载与转换
│   │   ├── strategies/  # 策略实现
│   │   ├── engines/     # 引擎模块
│   │   ├── services/    # 服务层
│   │   ├── api/         # API 路由
│   │   └── tests/       # 测试
│   └── pyproject.toml
├── frontend/            # Next.js 前端
│   ├── app/            # 页面路由
│   ├── components/     # React 组件
│   ├── lib/            # 工具库
│   └── package.json
├── data/               # 数据文件目录
└── README.md
```

## 核心功能 / Core Features

### 1. 策略系统 / Strategy System
- ✅ BaseStrategy 抽象基类
- ✅ MA Crossover 策略（均线交叉）
- ✅ MA Cluster Density 策略（均线密集开仓法）
- ✅ 策略配置系统（JSON序列化）

### 2. 回测引擎 / Backtest Engine
- ✅ 单/多策略回测
- ✅ 手续费和滑点模拟
- ✅ 绩效指标计算（收益、夏普、回撤、胜率等）
- ✅ 权益曲线生成

### 3. 行为引擎 / Behavior Engine
- ✅ 冲动指数计算
- ✅ 追涨杀跌指数
- ✅ 连续亏损检测
- ✅ 操作间隔统计

### 4. 混沌引擎 / Chaos Engine
- ✅ Lyapunov 指数近似计算
- ✅ 混沌指数（0-1）
- ✅ 波动率计算
- ✅ 噪音-信号比
- ✅ 市场状态分类（TREND/NEUTRAL/CHAOTIC）

### 5. 微结构引擎 / Microstructure Engine
- ✅ 鲸鱼活动指数
- ✅ 杠杆风险指数
- ✅ 成交量分析

### 6. 元策略引擎 / Meta Strategy Engine
- ✅ 综合多引擎指标
- ✅ 仓位倍数计算
- ✅ 交易开关决策
- ✅ 市场状态推荐

### 7. LLM 策略服务 / LLM Strategy Service
- ✅ 自然语言到策略配置的转换（占位实现）
- ✅ 支持中英文输入
- ✅ 策略模板映射

### 8. API 接口 / API Routes
- ✅ POST /api/v1/backtest/run - 运行回测
- ✅ GET  /api/v1/strategies - 列出策略
- ✅ POST /api/v1/strategies/from-llm - LLM生成策略
- ✅ GET  /api/v1/metrics/chaos - 混沌指标
- ✅ GET  /api/v1/metrics/behavior - 行为指标
- ✅ GET  /api/v1/metrics/regime - 市场状态

### 9. 前端界面 / Frontend UI
- ✅ 暗色主题
- ✅ 中英双语支持
- ✅ Dashboard 页面（策略表现）
- ✅ 策略管理页面
- ✅ 行为分析页面
- ✅ 图表可视化（权益曲线、回撤、混沌指数、状态时间轴）

## 快速开始 / Quick Start

### 后端启动 / Backend

```bash
cd backend
poetry install  # 或 uv sync
poetry run uvicorn app.main:app --reload
```

访问 API 文档: http://localhost:8000/docs

### 前端启动 / Frontend

```bash
cd frontend
npm install
npm run dev
```

访问前端: http://localhost:3000

## 数据准备 / Data Preparation

1. 将 OHLCV 数据文件放置到 `data/` 目录
2. 文件命名格式: `{SYMBOL}_{TIMEFRAME}.csv`
   - 例如: `BTCUSDT_1h.csv`
3. CSV 格式要求:
   ```
   timestamp,open,high,low,close,volume
   2024-01-01T00:00:00,42000.0,42500.0,41800.0,42300.0,1234.56
   ```

## 待完成功能 / TODO

以下功能已预留接口，待进一步实现：

1. **真实交易所API集成**
   - Binance/OKX API 客户端
   - 实时数据获取

2. **LLM API 真实集成**
   - OpenAI/DeepSeek API 连接
   - 策略代码生成

3. **数据库集成**
   - 策略配置持久化
   - 回测结果存储

4. **更多策略模板**
   - RSI 策略
   - MACD 策略
   - 布林带策略

5. **高级功能**
   - 多品种组合回测
   - 参数优化
   - 实时交易（模拟/实盘）

## 代码质量 / Code Quality

- ✅ 模块化设计
- ✅ 类型注解（Type Hints）
- ✅ Docstrings（中英文）
- ✅ 基础单元测试
- ✅ API 文档（FastAPI自动生成）

## 注意事项 / Notes

1. **LLM策略生成**：当前为占位实现，使用规则映射。真实LLM集成需要在 `services/llm_strategy_service.py` 中完成。

2. **交易所API**：数据加载器预留了接口，真实API集成需要在 `data/loader.py` 中实现。

3. **数据文件**：确保CSV数据文件格式正确，包含必需的列。

4. **环境变量**：后端需要配置 `.env` 文件（参考 `.env.example`）。

## 许可证 / License

本项目为示例/教学用途。

## 贡献 / Contribution

欢迎提交Issue和Pull Request！

