from typing import List, Optional

from pydantic import BaseModel, Field


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


class BirthChartInput(BaseModel):
    """八字排盘的输入参数"""

    birth_year: int = Field(description="出生年份，例如 2024", ge=1900, le=2100)
    birth_month: int = Field(description="出生月份，1-12 的整数", ge=1, le=12)
    birth_day: int = Field(
        description="出生日期，1-31 的整数，需符合实际月份天数", ge=1, le=31
    )
    birth_hour: int = Field(
        description="出生小时，0-23 的整数，使用24小时制", ge=0, le=23
    )

    gender: int = Field(
        description="性别，0 代表女性，1 代表男性", ge=0, le=1, default=0
    )

    now_year: Optional[int] = Field(
        description="当前年份，用作输出流月流日，例如 2024",
        ge=1900,
        le=2100,
        default=None,
    )
    now_month: Optional[int] = Field(
        description="当前月份，用作输出流月流日，1-12 的整数", ge=1, le=12, default=None
    )
    now_day: Optional[int] = Field(
        description="当前日期，用作输出流月流日，1-31 的整数，需符合实际月份天数",
        ge=1,
        le=31,
        default=None,
    )
    now_hour: Optional[int] = Field(
        description="当前小时，用作输出流月流日，0-23 的整数，使用24小时制",
        ge=0,
        le=23,
        default=None,
    )
