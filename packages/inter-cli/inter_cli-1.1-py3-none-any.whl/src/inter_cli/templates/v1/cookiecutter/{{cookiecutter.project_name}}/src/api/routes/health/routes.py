from fastapi import APIRouter, status
from api.routes.health.schemas import responses


router = APIRouter(
    prefix="/health",
    tags=["health check"],
)


@router.get(path="/", status_code=status.HTTP_200_OK)
async def health() -> responses.Health:
    return responses.Health(status="ok")
