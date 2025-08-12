"""Defines Pydantic models for validating application configuration.

Includes models for Google Sheets settings, document block settings,
and the overall application configuration schema.
"""


from pathlib import Path
from typing import List

from pydantic import BaseModel, Field


class GoogleSheetsConfig(BaseModel):
    """Configuration for Google Sheets integration.

    Attributes:
        spreadsheet_id: The ID of the Google Sheet to read from.
        time_zone: IANA time zone string used for date/time operations
            (e.g., "America/New_York").
        date_column_name: Name of the date column in the sheet. Defaults to "Date".
    """
    spreadsheet_id: str
    time_zone: str
    date_column_name: str = Field(default="Date")


class DocBlockConfig(BaseModel):
    """Configuration for a single document-generation block.

    Attributes:
        name: Human-readable identifier for this block (used in logs/UI).
        sheet_name: Name of the worksheet/tab to read data from.
        template_path: Filesystem path to the Jinja/Docs template used to render.
        block_title_template: Template for the generated block title.
        doc_id: Destination Google Doc ID to write into.
        enabled: Whether this block should be processed. Defaults to True.
    """
    name: str
    sheet_name: str
    template_path: Path
    block_title_template: str
    doc_id: str
    enabled: bool = True


class Config(BaseModel):
    """Top-level application configuration schema.

    Attributes:
        google_sheets: Settings for connecting to and reading Google Sheets.
        doc_blocks: Ordered list of document-generation blocks to process.
    """
    google_sheets: GoogleSheetsConfig
    doc_blocks: List[DocBlockConfig]
