from fastapi import FastAPI
from .routers import year
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum


app = FastAPI()

app.include_router(year.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://fredball.co.uk", "http://localhost:8080", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Hello World"}

handler = Mangum(app)