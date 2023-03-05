from fastapi import FastAPI, Response

from app.core.routers import router as api_router


app = FastAPI()


@app.get("/health-check")
def health_check():
    return Response(status_code=200)


app.include_router(api_router, prefix="/api/v1")
