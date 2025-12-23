# 占卜排盘 MCP

这是一个用于生成占卜排盘（当前主要实现：六爻 / Six-line）的 MCP Server

## 使用

### 依赖

- Python 3.12+
- uv

### 手动启动

#### 1. Clone the Repository

```bash
git clone https://github.com/wangsquirrel/divination-chart-mcp.git
cd divination-chart-mcp
```

#### 2. 安装依赖

```bash
uv sync
```

#### 3. 启动

```bash
uv run --with . divination-chart-mcp
```

### MCP 配置

```json
{
  "mcpServers": {
      "divination-chart-mcp": {
          "command": "uvx",
          "args": [
              "--from",
              "https://github.com/wangsquirrel/divination-chart-mcp.git",
              "divination-chart-mcp",
          ]
      }
  }
}
```

### 部署服务

- 使用asgi服务器，如uvicorn,可以直接启动sse服务
```bash
    uvicorn api.index:app --host 0.0.0.0 --port 3000
```
- 也可以直接在 Vercel 上部署这个项目，使用的是`vercel.json`配置文件。
