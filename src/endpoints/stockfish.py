from fastapi import APIRouter, Depends
from stockfish import Stockfish

from analyzer.analyzer import Analysis, GameAnalyzer
from dependencies.authentication import verify_api_key
from dependencies.stockfish import get_stockfish
from models.errors import Unauthorized
from models.stockfish import AnalyzePayload, BestMovePayload, BestMoveResponse, StatusResponse
from utils.const import MATE_MSG

router = APIRouter(prefix='/stockfish', tags=['stockfish'])


@router.get(
    path="/status/",
    response_model=StatusResponse,
)
async def get_chess_engine_status(stockfish: Stockfish = Depends(get_stockfish)) -> StatusResponse:
    return StatusResponse(
        version=stockfish.get_stockfish_major_version(),
        elo=stockfish.get_parameters()['UCI_Elo'],
        skill_level=stockfish.get_parameters()['Skill Level'],
        threads=stockfish.get_parameters()['Threads'],
    )


@router.post(
    path="/bestmove/",
    response_model=BestMoveResponse,
    deprecated=True,
)
async def get_best_move(payload: BestMovePayload, stockfish: Stockfish = Depends(get_stockfish)) -> BestMoveResponse:
    stockfish.set_fen_position(payload.fen_position)
    best_move = stockfish.get_best_move()

    return BestMoveResponse(
        move=best_move or MATE_MSG,
    )


@router.post(
    path='/analyze/',
    response_model=Analysis,
    dependencies=[Depends(verify_api_key)],
    responses={401: {'model': Unauthorized, 'description': 'User is unauthorized.'}},

)
def analyze_game(payload: AnalyzePayload, stockfish: Stockfish = Depends(get_stockfish)) -> Analysis:
    analyzer = GameAnalyzer(user=payload.user, stockfish=stockfish)
    return analyzer.get_analysis(game=payload.pgn)
