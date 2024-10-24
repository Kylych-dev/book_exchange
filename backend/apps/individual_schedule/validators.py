from pydantic import BaseModel, Field
from typing import List

class ScheduleDetail(BaseModel):
    week_day: str = Field(..., description="The day of the week")
    status: str = Field(..., description="Status of the day")
    hours: int = Field(..., description="Working hours")


class ScheduleData(BaseModel):
    name: str = Field(..., description="Schedule name")
    details: List[ScheduleDetail]
