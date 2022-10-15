
from fastapi import FastAPI, Request

from endpoints import stockfish
from settings import settings

app = FastAPI(
    title='FastFish',
    description='The webserver designed to provide analysis for chess games using stockfish chess engine.'
)
app.include_router(stockfish.router)


@app.middleware("http")
async def stockfish_version(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Stockfish-Version"] = settings.stockfish_version
    return response


@app.get("/")
async def root():
    return {"message": "Welcome to fastfish. FastAPI server based on chess engine - stockfish!"}
