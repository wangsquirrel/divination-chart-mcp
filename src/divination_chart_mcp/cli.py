import argparse
import logging

from fastmcp import FastMCP

from .server import fast_mcp

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run(fast_mcp: FastMCP, transport: str = None):
    """
    启动FastMCP服务器的辅助函数

    Args:
        fast_mcp: FastMCP实例
        transport: 传输方式，如果为None则从命令行参数读取
    """

    if transport is None:
        parser = argparse.ArgumentParser(description="启动FastMCP服务器")
        parser.add_argument(
            "--transport",
            "-t",
            type=str,
            default="stdio",
            choices=["stdio", "sse", "streamable-http"],
            help="服务器传输方式, 支持 stdio, sse, streamable-http",
        )
        args = parser.parse_args()
        transport = args.transport

    logger.info(f"启动{fast_mcp.name} FastMCP {transport}服务器...")
    try:
        fast_mcp.run(transport=transport)
        logger.info("FastMCP服务器运行结束")

    except Exception as e:
        logger.error(f"FastMCP服务器运行出错: {e}", exc_info=True)
        raise


def sixline():
    """CLI entry point for stdio transport"""
    run(fast_mcp, transport="stdio")


def all():
    """CLI entry point with transport selection"""
    run(fast_mcp)
