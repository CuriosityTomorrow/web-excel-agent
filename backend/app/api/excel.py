from fastapi import APIRouter, HTTPException, Response, Body
from fastapi.responses import StreamingResponse
import io
from typing import List
from app.models.excel import Workbook, UpdateCellRequest
from app.services.excel_service import excel_service

router = APIRouter(prefix='/api/excel', tags=['excel'])


@router.post('/workbook')
async def create_workbook(workbook: Workbook):
    """Create a new Excel workbook"""
    try:
        workbook_id = excel_service.create_workbook(workbook)
        return {'id': workbook_id, 'message': 'Workbook created successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/workbook/{workbook_id}')
async def get_workbook(workbook_id: str):
    """Get a workbook by ID"""
    workbook = excel_service.get_workbook(workbook_id)
    if not workbook:
        raise HTTPException(status_code=404, detail='Workbook not found')
    return workbook.dict()


@router.put('/workbook/{workbook_id}/cell')
async def update_cell(workbook_id: str, request: UpdateCellRequest):
    """Update a cell in a workbook"""
    try:
        workbook = excel_service.update_cell(
            workbook_id,
            request.sheet_index,
            request.row,
            request.col,
            request.value
        )
        return {'message': 'Cell updated successfully', 'data': workbook.dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/export/{workbook_id}')
async def export_excel(workbook_id: str):
    """Export workbook as Excel file with charts"""
    try:
        excel_data = excel_service.export_to_excel_with_charts(workbook_id)

        return StreamingResponse(
            io.BytesIO(excel_data),
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': f'attachment; filename=workbook_{workbook_id}.xlsx'}
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/{workbook_id}/chart')
async def add_chart_to_workbook(workbook_id: str, chart: dict):
    """Add a chart to the workbook for export"""
    try:
        excel_service.add_chart(workbook_id, chart)
        return {'message': 'Chart added successfully'}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/{workbook_id}/charts/batch')
async def add_charts_to_workbook(workbook_id: str, charts: List[dict] = Body(...)):
    """Add multiple charts and replace existing ones"""
    try:
        excel_service.set_workbook_charts(workbook_id, charts)
        return {'message': f'Added {len(charts)} charts successfully'}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/{workbook_id}/sync')
async def sync_workbook(workbook_id: str, workbook: Workbook):
    """Sync the entire workbook data from frontend to backend"""
    try:
        excel_service.sync_workbook(workbook_id, workbook)
        return {'message': 'Workbook synced successfully'}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
