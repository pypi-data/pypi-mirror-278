from __future__ import annotations

from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt


class ThresholdTypes(str, Enum):
    STATIC: Literal["static"] = "static"
    MOVING_AVERAGE: Literal["moving_average"] = "moving_average"


class StaticThresholdSettings(BaseModel):
    condition_above_value: Optional[float] = Field(description="Condition above value")
    condition_below_value: Optional[float] = Field(description="Condition below value")
    threshold_type: Literal["static"] = ThresholdTypes.STATIC.value


class MovingAverageThresholdSettings(BaseModel):
    is_violation_above: bool = True
    is_violation_below: bool = True
    violation_deviation: PositiveFloat
    threshold_type: Literal["moving_average"] = ThresholdTypes.MOVING_AVERAGE.value
    window_size: PositiveInt
