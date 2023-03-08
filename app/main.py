from fastapi import FastAPI, Response
from fastapi_pagination import add_pagination

from app.core.routers import router as api_router


app = FastAPI()


@app.get("/health-check")
def health_check():
    return {"status": "okay"}


app.include_router(api_router, prefix="/api/v1")
add_pagination(app)
