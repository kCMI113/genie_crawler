from pydantic_settings import BaseSettings


class DBConfig(BaseSettings):
    spotify_cid: str
    spotify_pwd: str
    db_host: str
    db_name: str
    db_username: str
    db_password: str
    input_path: str
    pl_file: str
    song_file: str

    class Config:
        env_file = ".env"
