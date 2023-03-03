from fastapi import FastAPI, Response


app = FastAPI()


@app.get("/health-check")
def health_check():
    return Response(status_code=200)
