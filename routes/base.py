from fastapi import FastAPI, APIRouter, Depends , status
from fastapi.responses import JSONResponse
from core.config import get_settings
import logging


base_router = APIRouter(
    prefix = "/api/v1",
    tags = ["api_v1"]
)

logger = logging.getLogger(__name__)

settings = get_settings()

@base_router.get("/healthcheck")
async def welcome():
    app_name = settings.APP_NAME
    app_version = settings.APP_VERSION

    return  JSONResponse(status_code=status.HTTP_200_OK,
                                     content={
                                             "App_Name" : app_name,
                                             "App_Version" : app_version,
                                     })
