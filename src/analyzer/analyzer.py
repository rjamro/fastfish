import io

from chess import pgn
from stockfish import Stockfish

from analyzer.enums import Pieces
from models.stockfish import Analysis


class GameAnalyzer(object):
    def __init__(self, stockfish: Stockfish, user: str):
        self.stockfish = stockfish
        self.user = user

    def get_analysis(self, game: str) -> Analysis:
        moves = []
        blunders = 0
        game_pgn = pgn.read_game(io.StringIO(game))
        user_pieces = self._get_user_pieces(game_pgn=game_pgn, user=self.user)
        self._initialize_board(game_pgn=game_pgn)
        for move_no, move in enumerate(game_pgn.mainline_moves()):
            # TODO verify if blunders are counted correctly
            if not self._is_move_correct(move=move) and self._is_user_turn(move_no=move_no, user_pieces=user_pieces):
                blunders += 1
            moves.append(move)
            self._set_new_position(moves=moves)
        return Analysis(blunders=blunders)

    def _initialize_board(self, game_pgn: pgn.Game) -> None:
        self.stockfish.set_fen_position(game_pgn.board().fen())

    def _set_new_position(self, moves: list[str]) -> None:
        self.stockfish.set_position(moves=moves)

    def _get_user_pieces(self, game_pgn: pgn.Game, user: str) -> Pieces:
        white_user = game_pgn.headers['White']
        return Pieces.WHITE if white_user == user else Pieces.BLACK

    def _is_move_correct(self, move: str) -> bool:
        return self.stockfish.is_move_correct(move)

    def _is_user_turn(self, move_no: int, user_pieces: Pieces) -> bool:
        return move_no % 2 and user_pieces == Pieces.BLACK
