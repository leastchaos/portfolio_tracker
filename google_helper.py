"""
To highlight some common use gspread functions
"""
from typing import Any

import gspread
import gspread_dataframe as gd
import pandas as pd

GOOGLE_CRED_LOCATION = "./credentials/google_service_cred.json"


def get_workbook(
    name: str,
    cred_location: str = GOOGLE_CRED_LOCATION,
) -> gspread.Spreadsheet:
    """
    get workbook
    """
    gc = gspread.service_account(filename=cred_location)
    return gc.open(name)


def set_sheet_with_df(
    workbook: gspread.Spreadsheet, sheet_name: str, dataframe: pd.DataFrame
) -> None:
    """
    set sheet with dataframe
    """
    worksheet = workbook.worksheet(sheet_name)
    worksheet.clear()
    gd.set_with_dataframe(worksheet, dataframe)


def update_cell(
    workbook: gspread.Spreadsheet, sheet_name: str, range: str, value: Any
) -> None:
    """
    update cell https://docs.gspread.org/en/latest/user-guide.html
    """
    worksheet = workbook.worksheet(sheet_name)
    worksheet.update_cell(range, value)
