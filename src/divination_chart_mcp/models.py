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
