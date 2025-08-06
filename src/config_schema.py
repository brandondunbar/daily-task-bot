from pydantic import BaseModel, Field
from typing import List
from pathlib import Path


class GoogleSheetsConfig(BaseModel):
    spreadsheet_id: str
    time_zone: str
    date_column_name: str = Field(default="Date")


class DocBlockConfig(BaseModel):
    name: str
    sheet_name: str
    template_path: Path
    block_title_template: str
    doc_id: str
    enabled: bool = True


class Config(BaseModel):
    google_sheets: GoogleSheetsConfig
    doc_blocks: List[DocBlockConfig]
