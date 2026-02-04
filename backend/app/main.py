from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, excel, scraper, chart

app = FastAPI(
    title='Web Excel Agent API',
    description='AI-powered Excel web application with web scraping capabilities',
    version='0.1.0'
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'http://127.0.0.1:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Include routers
app.include_router(chat.router)
app.include_router(excel.router)
app.include_router(scraper.router)
app.include_router(chart.router)


@app.get('/')
async def root():
    return {
        'message': 'Web Excel Agent API',
        'version': '0.1.0',
        'docs': '/docs',
        'endpoints': {
            'chat': '/api/chat',
            'excel': '/api/excel',
            'scrape': '/api/scrape',
            'chart': '/api/chart',
        }
    }


@app.get('/health')
async def health_check():
    return {'status': 'healthy'}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
