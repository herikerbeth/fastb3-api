from fastapi import FastAPI

app = FastAPI(
    title="FastB3 API",
    description="API RESTful for consulting B3 stock quotes",
    version="1.0.0"
)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to FastB3 API"}