# 占卜排盘 MCP

这是一个用于生成占卜排盘（当前主要实现：六爻(Six-line)和八字(Bazi)）的 MCP Server。

## 使用

### 依赖

- Python 3.12+
- uv

### 本地运行

#### 1. Clone the repository

```bash
git clone https://github.com/wangsquirrel/divination-chart-mcp.git
cd divination-chart-mcp
```

#### 2. 安装依赖

```bash
uv sync
```

#### 3. 启动 stdio MCP server

```bash
uv run --with . divination-chart-mcp
```

也可以显式指定 transport:

```bash
uv run --with . divination-chart-mcp --transport stdio
uv run --with . divination-chart-mcp --transport sse
uv run --with . divination-chart-mcp --transport streamable-http
```

### 用 uvx 启动

本地仓库:

```bash
uvx --from . divination-chart-mcp
```

直接从 GitHub:

```bash
uvx --from git+https://github.com/wangsquirrel/divination-chart-mcp divination-chart-mcp
```

### MCP 配置

```json
{
  "mcpServers": {
    "divination-chart-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/wangsquirrel/divination-chart-mcp",
        "divination-chart-mcp"
      ]
    }
  }
}
```

### 测试MCP服务

```bash
uvx fastmcp list --command  'uv run --with . divination-chart-mcp' --json
```

### 部署服务

- 使用 ASGI 服务器启动 SSE 服务:

```bash
uvicorn api.index:app --host 0.0.0.0 --port 3000
```


- `api/index.py` 导出了同一个 ASGI app，可用于云平台部署
- 也可以直接在 Vercel 上部署这个项目，使用的是 `vercel.json` 配置文件
