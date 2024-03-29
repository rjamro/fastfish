import io

from chess import pgn
from stockfish import Stockfish

from analyzer.enums import Pieces
from models.stockfish import Analysis


class GameAnalyzer(object):
    def __init__(self, user: str, stockfish: Stockfish):
        self.stockfish = stockfish
        self.user = user

    def get_analysis(self, game: str) -> Analysis:
        moves = []
        blunders = 0
        moves_counter = 0
        game_pgn = self._get_pgn_game(game=game)
        user_pieces = self._get_user_pieces(game_pgn=game_pgn, user=self.user)

        self._initialize_board(game_pgn=game_pgn)
        for move_no, move in enumerate(game_pgn.mainline_moves()):
            if self._is_blunder(move=move, move_no=move_no, user_pieces=user_pieces):
                blunders += 1
            moves.append(move)
            self._set_new_position(moves=moves)
            moves_counter += 1
        return Analysis(blunders=blunders, total_moves=moves_counter // 2)

    def _initialize_board(self, game_pgn: pgn.Game) -> None:
        self.stockfish.set_fen_position(game_pgn.board().fen())

    def _set_new_position(self, moves: list[str]) -> None:
        self.stockfish.set_position(moves=moves)

    def _get_user_pieces(self, game_pgn: pgn.Game, user: str) -> Pieces:
        white_user = game_pgn.headers['White']
        return Pieces.WHITE if white_user == user else Pieces.BLACK

    def _get_pgn_game(self, game: str) -> pgn.Game:
        return pgn.read_game(io.StringIO(game))

    def _is_blunder(self, move: str, move_no: int, user_pieces: int) -> bool:
        return self._is_user_turn(move_no=move_no, user_pieces=user_pieces) and not self._is_move_correct(move=move)

    def _is_move_correct(self, move: str) -> bool:
        top_moves = [move['Move'] for move in self.stockfish.get_top_moves()]
        return move in top_moves

    def _is_user_turn(self, move_no: int, user_pieces: Pieces) -> bool:
        return move_no % 2 and user_pieces == Pieces.BLACK
