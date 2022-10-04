from stockfish import Stockfish

from settings import settings


async def get_stockfish() -> Stockfish:
    return Stockfish(settings.stockfish_path)
