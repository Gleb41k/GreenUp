from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.middleware.last_login import LastLoginMiddleware

app = FastAPI(title=settings.APP_PROJECT)

app.add_middleware(LastLoginMiddleware)

app.include_router(api_router, prefix=settings.APP_API_V1_STR)


@app.get("/")
def root():
    return {"message": "FastAPI Enterprise Ready!"}
