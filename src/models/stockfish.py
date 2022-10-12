from pydantic import BaseModel, Field


class BestMovePayload(BaseModel):
    fen_position: str = Field(default='rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2')


class BestMoveResponse(BaseModel):
    move: str = Field(default='d2d4')


class StatusResponse(BaseModel):
    version: str = Field(default='20122')
    elo: int = Field(default=2800)
    skill_level: int = Field(default=20)
    threads: int = Field(default=1)


class AnalyzePayload(BaseModel):
    pgn: str
    user: str


class Analysis(BaseModel):
    blunders: int
