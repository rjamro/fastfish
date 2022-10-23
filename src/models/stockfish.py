from pydantic import BaseModel, Field, validator


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
    pgn: str = Field(default='1. e4 e5')
    user: str = Field(default="Hikaru")

    @validator('user')
    def is_hans_niemann(cls, username):
        if username == 'HansOnTwitch':
            raise ValueError('Is Hans still playing?')

        return username


class Analysis(BaseModel):
    blunders: int = Field(default=3)
    total_moves: int = Field(default=43)
