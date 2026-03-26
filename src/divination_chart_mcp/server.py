import logging
from datetime import datetime

from divicast.birth_chart.birth import BirthChart
from divicast.birth_chart.output import StandardBirthChartOutput
from divicast.birth_chart.output import to_standard_format as bazi_to_standard_format
from divicast.entities.misc import Gender
from divicast.sixline import DivinatorySymbol  # type: ignore
from divicast.sixline import to_standard_format
from divicast.sixline.output import (  # type: ignore
    StandardDivinatorySymbolOutput,
    to_standard_format,
)
from fastmcp import FastMCP

from .models import BirthChartInput, DivinationInput

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

fast_mcp = FastMCP(
    name="divination-charting-mcp",
    instructions="占卜排盘工具，提供六爻和八字排盘功能",
    dereference_schemas=True,
)

fast_mcp2 = FastMCP(
    name="sixline",
    instructions="六爻排盘工具",
    dereference_schemas=True,
)


@fast_mcp.tool()
@fast_mcp2.tool()
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


@fast_mcp.tool()
def divination_bazi(
    input_data: BirthChartInput,
) -> StandardBirthChartOutput:
    """
    八字排盘工具 - 根据年月日时及性别，进行八字排盘，返回八字盘面的详细信息和启发性的分析。
    """

    dt = datetime(
        year=input_data.birth_year,
        month=input_data.birth_month,
        day=input_data.birth_day,
        hour=input_data.birth_hour,
    )
    gender = Gender.Male if input_data.gender == 1 else Gender.Female
    target_dt = datetime.now()
    if (
        input_data.now_year
        and input_data.now_month
        and input_data.now_day
        and input_data.now_hour
    ):
        target_dt = datetime(
            year=input_data.now_year,
            month=input_data.now_month,
            day=input_data.now_day,
            hour=input_data.now_hour,
        )
    return bazi_to_standard_format(
        BirthChart.create(dt=dt, gender=gender), target_dt=target_dt
    )
