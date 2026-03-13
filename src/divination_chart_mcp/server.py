import logging
from datetime import datetime

from divicast.sixline import DivinatorySymbol  # type: ignore
from divicast.sixline import to_standard_format
from divicast.sixline.output import StandardDivinatorySymbolOutput  # type: ignore
from fastmcp import FastMCP

from .models import DivinationInput

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

fast_mcp = FastMCP(
    name="divination-charting-mcp",
    instructions="占卜排盘的MCP服务器",
    dereference_schemas=True,
)


@fast_mcp.tool()
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
