
from fastapi import Depends, FastAPI, Request
from stockfish import Stockfish
from analyzer.analyzer import Analysis, GameAnalyzer
from settings import settings
from dependencies.stockfish import get_stockfish
from models.stockfish import AnalyzePayload, BestMovePayload, BestMoveResponse, StatusResponse
from utils.const import MATE_MSG

app = FastAPI()


@app.middleware("http")
async def stockfish_version(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Stockfish-Version"] = settings.stockfish_version
    return response


@app.get("/")
async def root():
    return {"message": "Welcome to fastfish. FastAPI server based on chess engine - stockfish!"}


@app.get("/status/", response_model=StatusResponse)
async def get_chess_engine_status(stockfish: Stockfish = Depends(get_stockfish)) -> StatusResponse:
    return StatusResponse(
        version=stockfish.get_stockfish_major_version(),
        elo=stockfish.get_parameters()['UCI_Elo'],
        skill_level=stockfish.get_parameters()['Skill Level'],
        threads=stockfish.get_parameters()['Threads'],
    )


@app.post("/bestmove/", response_model=BestMoveResponse)
async def get_best_move(payload: BestMovePayload, stockfish: Stockfish = Depends(get_stockfish)) -> BestMoveResponse:
    stockfish.set_fen_position(payload.fen_position)
    best_move = stockfish.get_best_move()

    return BestMoveResponse(
        move=best_move or MATE_MSG,
    )


@app.post('/analyze/', response_model=Analysis)
async def analyze_game(payload: AnalyzePayload, stockfish: Stockfish = Depends(get_stockfish)) -> Analysis:
    analyzer = GameAnalyzer(stockfish=stockfish, user=payload.user)
    return analyzer.get_analysis(game=payload.pgn)
