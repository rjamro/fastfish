from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    stockfish_path: str = Field(default='/usr/local/bin/stockfish')
    stockfish_version: str = Field(default='14.1')

    api_key: str

    @validator('api_key')
    def is_api_key_valid(cls, api_key: str | None) -> str:
        if len(api_key) < 32:
            raise ValueError('API KEY is too short and not safe enough.')
        return api_key

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
