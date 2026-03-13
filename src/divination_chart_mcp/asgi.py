from .server import fast_mcp

app = fast_mcp.http_app(transport="sse")
