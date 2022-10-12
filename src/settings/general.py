from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    stockfish_path: str = Field(default='/usr/local/bin/stockfish')
    stockfish_version: str = Field(default='14.1')


settings = Settings()
