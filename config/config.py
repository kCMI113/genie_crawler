from pydantic_settings import BaseSettings
from datetime import datetime

class DBConfig(BaseSettings):
    spotify_cid: str
    spotify_pwd: str
    db_host: str
    db_name: str
    db_username: str
    db_password: str
    input_path: str = "migration/input"
    pl_file: str = "playlists_0721.csv"
    song_file: str = "join_songs_0726_unique.csv"
    query_date: datetime = datetime.utcnow()

    class Config:
        env_file = ".env"

class GenieConfig(BaseSettings):
    start_idx: int = 1
    query_date: datetime = datetime.utcnow()
    img_resize: int = 244
    max_resize: int = 600