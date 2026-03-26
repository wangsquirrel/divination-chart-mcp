本文件为 Claude Code (claude.ai/code) 提供在此代码库中工作的指导。

## 项目概述

这是一个用于生成占卜排盘的 MCP (Model Context Protocol) 服务器。目前实现六爻排盘和八字排盘。

## 常用命令

```bash
# 安装依赖
uv sync

# 运行 stdio 传输的 MCP 服务器（默认）
uv run --with . divination-chart-mcp

# 指定传输方式运行
uv run --with . divination-chart-mcp --transport stdio
uv run --with . divination-chart-mcp --transport sse
uv run --with . divination-chart-mcp --transport streamable-http

# 测试 MCP 服务器
uvx fastmcp list --command 'uv run --with . divination-chart-mcp' --json

# 运行客户端示例
uv run python examples/mcp_client.py

# 使用 uvicorn 部署
uvicorn api.index:app --host 0.0.0.0 --port 3000
```

## 架构

```
divination-chart-mcp/
├── src/divination_chart_mcp/          # 主包
│   ├── server.py                      # FastMCP 服务器 + @fast_mcp.tool() 定义
│   ├── models.py                      # Pydantic 输入模型
│   ├── cli.py                         # CLI 入口点 (sixline, all)
│   └── asgi.py                        # ASGI 应用导出（用于部署）
├── api/index.py                       # Vercel 部署入口
└── examples/
    ├── mcp_client.py                  # 演示如何调用工具
    └── start_server.py                # 简单的服务器启动脚本
```

**核心模式**：`server.py` 定义 `@fast_mcp.tool()` 函数，使用外部 `divicast` 库进行占卜逻辑。工具接收 `models.py` 中的 Pydantic 模型作为输入，返回类型化输出。

**Divicast 库** (`divicast @ git+https://github.com/wangsquirrel/divicast.git@v0.2.1`) 提供：
- `divicast.sixline.DivinatorySymbol` - 六爻占卜
- `divicast.sixline.to_standard_format()` - 输出格式化
- 计划中：`divicast.bazi.BaziSymbol` - 八字排盘

## 关键文件

- `server.py:23-37` - `divination_liu_yao` 工具定义（当前唯一的 MCP 工具）
- `models.py:5-18` - `DivinationInput` 模型，包含 year/month/day/hour/yaogua
- `pyproject.toml:11-16` - 依赖配置，包括 divicast git 包

## 开发注意事项

- 包使用 `uv_build` 构建，目标是 wheel
- CLI 脚本定义在 `pyproject.toml [project.scripts]`：
  - `sixline` → `cli:sixline`（stdio 传输）
  - `divination-chart-mcp` → `cli:all`（交互式选择传输方式）
- FastMCP 使用 `dereference_schemas=True` 以获得更扁平的 schema 输出