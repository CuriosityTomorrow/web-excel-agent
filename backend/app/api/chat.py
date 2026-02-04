from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.agent_service import agent_service

router = APIRouter(prefix='/api/chat', tags=['chat'])


class ChatRequest(BaseModel):
    message: str


@router.post('')
async def chat(request: ChatRequest):
    """Process chat message and return AI response"""
    try:
        response = agent_service.process_message(request.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
