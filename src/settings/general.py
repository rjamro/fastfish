from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    stockfish_path: str = Field(default='/usr/local/bin/stockfish')


settings = Settings()
