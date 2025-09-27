from fastapi import APIRouter
from pydantic import BaseModel
from src.agents.workflows.book_workflow import stream_workflow
from fastapi.responses import StreamingResponse

router = APIRouter()

class CreateBookRequest(BaseModel):
    title: str

@router.post("/create-book")
async def create_book(request: CreateBookRequest):
    return StreamingResponse(
        stream_workflow(book_title=request.title),
        media_type="text/event-stream"
    )