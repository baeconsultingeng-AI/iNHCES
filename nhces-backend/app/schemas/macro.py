from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class MacroVariable(BaseModel):
    variable:   str
    label:      str
    value:      float
    unit:       str
    as_of_date: Optional[str] = None
    source:     str
    data_level: str  # GREEN | AMBER | RED


class MacroSnapshot(BaseModel):
    variables:         list[MacroVariable]
    overall_freshness: str
    as_of:             datetime


class MacroHistoryPoint(BaseModel):
    year:  int
    value: float


class MacroHistory(BaseModel):
    variable:   str
    label:      str
    unit:       str
    data_level: str
    data:       list[MacroHistoryPoint]
