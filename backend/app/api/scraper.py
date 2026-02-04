from fastapi import APIRouter, HTTPException, Body
from app.services.scraper_service import scraper_service
from pydantic import BaseModel

router = APIRouter(prefix='/api/scrape', tags=['scraper'])


class ScrapeRequest(BaseModel):
    url: str
    table_index: int = 0


@router.post('/table')
async def scrape_table(request: ScrapeRequest):
    """Scrape a table from a webpage"""
    try:
        sheet = scraper_service.scrape_table(request.url, request.table_index)
        return {
            'message': f'Successfully scraped table with {len(sheet.rows)} rows',
            'data': sheet.dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/list')
async def scrape_list(url: str = Body(..., embed=True), list_index: int = Body(0, embed=True)):
    """Scrape a list from a webpage"""
    try:
        sheet = scraper_service.scrape_list(url, list_index)
        return {
            'message': f'Successfully scraped list with {len(sheet.rows)} items',
            'data': sheet.dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
