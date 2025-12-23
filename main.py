import argparse
import json
import logging
from datetime import datetime
from typing import List, Optional

from divicast.sixline import DivinatorySymbol  # type: ignore
from divicast.sixline import to_standard_format
from divicast.sixline.output import StandardDivinatorySymbolOutput  # type: ignore
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DivinationInput(BaseModel):
    """六爻排盘的输入参数，公历的年月日时24时制数字数字"""

    year: int = Field(description="年份，例如 2024", ge=1900, le=2100)
    month: int = Field(description="月份，1-12 的整数", ge=1, le=12)
    day: int = Field(description="日期，1-31 的整数，需符合实际月份天数", ge=1, le=31)
    hour: int = Field(description="小时，0-23 的整数，使用24小时制", ge=0, le=23)

    yaogua: Optional[List[int]] = Field(
        default=None,
        description="摇卦结果数组，从初爻到上爻排列, 数字代表硬币背面的个数，范围从0-3。如果不提供，就自动摇卦",
        min_length=6,
        max_length=6,
    )


def divination_liu_yao(
    input_data: DivinationInput,
) -> StandardDivinatorySymbolOutput:
    """
    六爻排盘工具 - 根据年月日时进行六爻占卜排盘，返回六爻盘面的详细信息。
    """

    now = datetime(
        year=input_data.year,
        month=input_data.month,
        day=input_data.day,
        hour=input_data.hour,
    )
    return to_standard_format(DivinatorySymbol.create(cnts=input_data.yaogua, now=now))


def sixline():

    fast_mcp = FastMCP(
        name="liu-yao-mcp",
        instructions="根据时间进行六爻排盘的MCP服务器",
    )

    description_with_output_schema = (
        "六爻排盘工具 - 根据年月日时进行六爻占卜排盘，返回六爻盘面的详细信息。返回结果遵循以下JSON Schema定义:\n"
        + f"""{json.dumps(StandardDivinatorySymbolOutput.model_json_schema(), ensure_ascii=False)}"""
    )

    fast_mcp.tool(description=description_with_output_schema)(divination_liu_yao)
    run(fast_mcp)


def all():

    fast_mcp = get_fast_mcp()
    run(fast_mcp)


def get_fast_mcp() -> FastMCP:
    """
    创建并返回一个FastMCP实例
    """
    fast_mcp = FastMCP(
        name="divination-charting-mcp",
        instructions="占卜排盘的MCP服务器",
    )
    description_with_output_schema = (
        "六爻排盘工具 - 根据年月日时进行六爻占卜排盘，返回六爻盘面的详细信息。返回结果遵循以下JSON Schema定义:\n"
        + f"""{json.dumps(StandardDivinatorySymbolOutput.model_json_schema(), ensure_ascii=False)}"""
    )

    fast_mcp.tool(description=description_with_output_schema)(divination_liu_yao)
    return fast_mcp


def run(fast_mcp: FastMCP):
    """
    启动FastMCP服务器的辅助函数
    """

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

    logger.info(f"启动{fast_mcp.name} FastMCP {args.transport}服务器...")
    try:
        fast_mcp.run(transport=args.transport)
        logger.info("FastMCP服务器运行结束")

    except Exception as e:
        logger.error(f"FastMCP服务器运行出错: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    all()
