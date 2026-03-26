#!/usr/bin/env python3

import asyncio
import logging
import sys
from pathlib import Path

from fastmcp import Client
from mcp.types import TextContent

from divination_chart_mcp.server import fast_mcp

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


async def test_mcp_server():
    """通过 FastMCP 客户端直接连接本进程内的 server。"""

    logger.info("连接到MCP服务器实例...")
    try:
        async with Client(fast_mcp) as client:
            logger.info("获取工具列表...")
            tools = await asyncio.wait_for(client.list_tools(), timeout=10.0)
            logger.info(f"服务器提供了 {len(tools)} 个工具:")

            for tool in tools:
                logger.info(f"- 工具名称: {tool.name}")
                logger.info(f"  描述: {tool.description}")
                logger.info(f"  输入Schema: {tool.inputSchema}")
                logger.info(f"  输出Schema: {tool.outputSchema}")

            if tools:
                tool_name = tools[1].name
                logger.info(f"\n调用工具: {tool_name}")
                arguments = {}
                if tool_name == "divination_liu_yao":
                    arguments = {
                        "input_data": {
                            "year": 2024,
                            "month": 9,
                            "day": 19,
                            "hour": 15,
                            "yaogua": [0, 1, 1, 2, 1, 3],
                        }
                    }
                elif tool_name == "divination_bazi":
                    arguments = {
                        "input_data": {
                            "birth_year": 1990,
                            "birth_month": 5,
                            "birth_day": 20,
                            "birth_hour": 10,
                            "gender": 1,
                            "now_year": 2024,
                            "now_month": 9,
                            "now_day": 19,
                            "now_hour": 15,
                        }
                    }

                logger.info(f"参数: {arguments}")
                result = await asyncio.wait_for(
                    client.call_tool(tool_name, arguments), timeout=30.0
                )
                logger.info("工具调用结果:")

                for item in result.content:
                    if isinstance(item, TextContent):
                        logger.info(item.text)
                    else:
                        logger.info(f"非文本内容: {item}")

                logger.info("测试完成，成功调用工具并获取结果。")
            else:
                logger.warning("服务器未提供任何工具")

    except asyncio.TimeoutError:
        logger.error("操作超时，请检查MCP服务器是否正常运行")
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
