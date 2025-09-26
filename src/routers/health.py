from fastapi.routing import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthRequest(BaseModel):
    message: str

class HealthResponse(BaseModel):
    status: str

@router.get("/health", tags=["Health"])
def health_check(request: HealthRequest) -> HealthResponse:
    try:
        # Simulate a health check operation
        # In a real scenario, you might check database connectivity, external service status, etc.
        # If everything is fine, return OK status
        return HealthResponse(status="OK")
    except Exception as e:
        return HealthResponse(status=f"Error: {str(e)}")