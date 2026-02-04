from pydantic import BaseModel
from typing import List, Optional


class Cell(BaseModel):
    row: int
    col: int
    value: str


class Sheet(BaseModel):
    name: str
    rows: List[List[str]]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Sheet1",
                "rows": [
                    ["Name", "Age", "City"],
                    ["Alice", "30", "New York"],
                    ["Bob", "25", "London"],
                ]
            }
        }


class Workbook(BaseModel):
    id: Optional[str] = None
    sheets: List[Sheet]
    active_sheet: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "sheets": [
                    {
                        "name": "Sheet1",
                        "rows": [["A1", "B1"], ["A2", "B2"]],
                    }
                ],
                "active_sheet": 0,
            }
        }


class UpdateCellRequest(BaseModel):
    sheet_index: int
    row: int
    col: int
    value: str


class ChartConfig(BaseModel):
    type: str  # bar, line, pie
    title: Optional[str] = None
    data: List[dict]
    columns: Optional[List[str]] = None
