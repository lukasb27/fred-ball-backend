from fastapi import FastAPI
from .routers import year

import json

app = FastAPI()

app.include_router(year.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}