"""
MCP Tools for Excel operations
These tools can be used by the AI Agent to perform Excel-related tasks
"""
from typing import Dict, Any
from app.services.excel_service import excel_service
from app.models.excel import Workbook


def create_excel_workbook(sheets_data: list) -> str:
    """
    Create a new Excel workbook

    Args:
        sheets_data: List of sheet data with name and rows

    Returns:
        Workbook ID

    Example:
        >>> create_excel_workbook([{
        ...     "name": "Sheet1",
        ...     "rows": [["A1", "B1"], ["A2", "B2"]]
        ... }])
    """
    sheets = []
    for sheet_data in sheets_data:
        from app.models.excel import Sheet
        sheets.append(Sheet(**sheet_data))

    workbook = Workbook(sheets=sheets)
    workbook_id = excel_service.create_workbook(workbook)
    return workbook_id


def read_excel_data(workbook_id: str) -> Dict[str, Any]:
    """
    Read Excel data from workbook

    Args:
        workbook_id: ID of the workbook

    Returns:
        Workbook data including all sheets
    """
    workbook = excel_service.get_workbook(workbook_id)
    if not workbook:
        raise ValueError(f"Workbook {workbook_id} not found")
    return workbook.dict()


def update_cell(workbook_id: str, sheet_index: int, row: int, col: int, value: str) -> Dict[str, Any]:
    """
    Update a specific cell in the workbook

    Args:
        workbook_id: ID of the workbook
        sheet_index: Index of the sheet (0-based)
        row: Row index (0-based)
        col: Column index (0-based)
        value: New value for the cell

    Returns:
        Updated workbook data
    """
    workbook = excel_service.update_cell(workbook_id, sheet_index, row, col, value)
    return workbook.dict()


def add_sheet(workbook_id: str, sheet_name: str) -> Dict[str, Any]:
    """
    Add a new sheet to the workbook

    Args:
        workbook_id: ID of the workbook
        sheet_name: Name for the new sheet

    Returns:
        Updated workbook data
    """
    workbook = excel_service.add_sheet(workbook_id, sheet_name)
    return workbook.dict()


def export_excel_file(workbook_id: str, filename: str = None) -> bytes:
    """
    Export workbook as Excel file (binary data)

    Args:
        workbook_id: ID of the workbook
        filename: Optional filename for the export

    Returns:
        Excel file as bytes
    """
    excel_data = excel_service.export_to_excel(workbook_id)
    return excel_data


# Register MCP tools
MCP_TOOLS = {
    'create_excel_workbook': create_excel_workbook,
    'read_excel_data': read_excel_data,
    'update_cell': update_cell,
    'add_sheet': add_sheet,
    'export_excel_file': export_excel_file,
}
