from fastapi import APIRouter, HTTPException
from app.models.excel import ChartConfig
from app.services.chart_service import chart_service

router = APIRouter(prefix='/api/chart', tags=['chart'])


@router.post('')
async def create_chart(config: ChartConfig):
    """Create a chart configuration"""
    try:
        chart = chart_service.create_chart(
            config.type,
            config.data,
            config.title,
            config.columns
        )
        return {
            'message': 'Chart created successfully',
            'type': 'chart',
            'data': chart
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
