# SuperQuantLab 2.0 启动指南 / Startup Guide

## 快速启动 / Quick Start

### 1. 启动后端 / Start Backend

#### Windows:
```bash
cd backend
start.bat
```

#### Linux/Mac:
```bash
cd backend
chmod +x start.sh
./start.sh
```

#### 手动启动 / Manual:
```bash
cd backend

# 使用 Poetry
poetry install
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或使用 uv
uv sync
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端将在 http://localhost:8000 启动
API 文档: http://localhost:8000/docs

### 2. 启动前端 / Start Frontend

```bash
cd frontend
npm install  # 如果还没安装依赖
npm run dev
```

前端将在 http://localhost:3000 启动

## 演示数据 / Demo Data

系统已配置为在没有真实数据时自动使用演示数据，包括：

- ✅ 示例策略（MA Crossover, MA Cluster）
- ✅ 权益曲线数据
- ✅ 混沌指数数据
- ✅ 行为指标数据
- ✅ 市场状态信息

所有 API 端点都会在无法加载真实数据时返回演示数据，确保前端功能可以正常展示。

## 数据文件 / Data Files

如果你想使用真实数据，将 CSV 文件放到 `data/` 目录：

格式: `{SYMBOL}_{TIMEFRAME}.csv`

示例: `BTCUSDT_1h.csv`

CSV 格式要求：
```
timestamp,open,high,low,close,volume
2024-01-01T00:00:00,42000.0,42500.0,41800.0,42300.0,1234.56
```

## 访问页面 / Pages

- 首页: http://localhost:3000
- 策略表现: http://localhost:3000/dashboard
- 策略管理: http://localhost:3000/strategies
- 行为分析: http://localhost:3000/behavior

## 故障排除 / Troubleshooting

### 后端无法启动
- 检查是否安装了依赖: `poetry install` 或 `uv sync`
- 检查 Python 版本 (需要 3.11+)
- 查看错误日志

### 前端无法连接后端
- 确认后端在 http://localhost:8000 运行
- 检查浏览器控制台错误
- 确认 CORS 配置正确

### 没有数据显示
- 系统会自动使用演示数据
- 检查浏览器网络请求
- 查看后端日志

## 环境变量 / Environment Variables

后端 `.env` 文件（可选）:
```
API_V1_PREFIX=/api/v1
HOST=0.0.0.0
PORT=8000
LLM_API_KEY=your_key_here
CORS_ORIGINS=["http://localhost:3000"]
```

前端 `.env.local` 文件（可选）:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

