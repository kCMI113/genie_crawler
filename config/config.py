from pydantic_settings import BaseSettings


class DBConfig(BaseSettings):
    spotify_cid: str
    spotify_pwd: str
    db_host: str
    db_name: str
    db_username: str
    db_password: str
    input_path: str = "migration/input"
    pl_file: str = "playlists_0721.csv"
    song_file: str = "join_songs_0726.csv"

    class Config:
        env_file = ".env"
