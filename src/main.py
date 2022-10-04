
from fastapi import Depends, FastAPI
from stockfish import Stockfish

from dependencies.stockfish import get_stockfish
from models.stockfish import BestMovePayload, BestMoveResponse, StatusResponse
from utils.const import MATE_INFO

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to fastfish. FastAPI server based on chess engine - stockfish!"}


@app.get("/status/", response_model=StatusResponse)
async def stockfish_status(stockfish: Stockfish = Depends(get_stockfish)) -> StatusResponse:
    return StatusResponse(
        version=stockfish.get_stockfish_major_version(),
    )


@app.get("/bestmove/", response_model=BestMoveResponse)
async def get_best_move(payload: BestMovePayload, stockfish: Stockfish = Depends(get_stockfish)) -> BestMoveResponse:
    stockfish.set_fen_position(payload.fen_position)
    best_move = stockfish.get_best_move()

    return BestMoveResponse(
        move=best_move or MATE_INFO,
    )
