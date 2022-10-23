from stockfish import Stockfish

from settings import settings


def get_stockfish() -> Stockfish:
    stockfish = Stockfish(settings.stockfish_path)
    stockfish.update_engine_parameters({
        'Threads': 4,
        'Minimum Thinking Time': 1,
    })
    return stockfish
