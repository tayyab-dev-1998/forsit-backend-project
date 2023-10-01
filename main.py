from fastapi import FastAPI

from api.api import api_router

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def main():
    return {"message": "Hello world"}
