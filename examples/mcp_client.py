#!/usr/bin/env python3

import asyncio
import logging
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import TextContent, Tool

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


async def test_mcp_server():
    """测试MCP服务器"""
    # 获取项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    python_path = sys.executable
    mcp_server_path = os.path.join(project_root, "../main.py")

    logger.info(f"Python路径: {python_path}")
    logger.info(f"MCP服务器路径: {mcp_server_path}")

    if not os.path.exists(mcp_server_path):
        logger.error(f"MCP服务器文件不存在: {mcp_server_path}")
        return

    # 配置服务器参数
    server_params = StdioServerParameters(
        command=python_path,
        args=[mcp_server_path],
    )

    logger.info("连接到MCP服务器...")
    try:
        async with stdio_client(server=server_params) as (read, write):
            logger.info("创建客户端会话...")
            # 创建客户端会话
            async with ClientSession(read, write) as client:
                try:
                    await asyncio.wait_for(client.initialize(), timeout=30.0)

                except asyncio.TimeoutError:
                    logger.error(
                        "客户端初始化超时（30秒），可能是服务器未正确启动或通信问题"
                    )
                    return
                except Exception as e:
                    logger.error(f"客户端初始化过程中发生错误: {e}", exc_info=True)
                    return

                # 列出工具（设置超时）
                logger.info("获取工具列表...")
                tools_result = await asyncio.wait_for(client.list_tools(), timeout=10.0)
                tools = tools_result.tools
                logger.info(f"服务器提供了 {len(tools)} 个工具:")

                for tool in tools:
                    logger.info(f"- 工具名称: {tool.name}")
                    logger.info(f"  描述: {tool.description}")
                    logger.info(f"  输入Schema: {tool.inputSchema}")

                # 调用工具
                if tools:
                    tool_name = tools[0].name
                    logger.info(f"\n调用工具: {tool_name}")

                    # 准备测试参数
                    arguments = {
                        "input_data": {
                            "year": 2024,
                            "month": 9,
                            "day": 19,
                            "hour": 15,
                            "yaogua": [0, 1, 1, 2, 1, 3],
                        }
                    }

                    logger.info(f"参数: {arguments}")
                    result = await asyncio.wait_for(
                        client.call_tool(tool_name, arguments), timeout=30.0
                    )
                    logger.info("工具调用结果:")

                    for item in result:
                        if isinstance(item, TextContent):
                            logger.info(item.text)
                        else:
                            logger.info(f"非文本内容: {item}")
                else:
                    logger.warning("服务器未提供任何工具")

    except asyncio.TimeoutError:
        logger.error("操作超时，请检查MCP服务器是否正常运行")
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
