from pydantic_settings import BaseSettings
from datetime import datetime


class GenieConfig(BaseSettings):
    # common
    query_date: datetime = datetime.utcnow()

    # crawling start genie_id of playlist
    use_latest_start_idx: bool = False
    start_idx: int = 1

    # for image
    img_resize: int = 244
    max_resize: int = 600

    # for DB
    spotify_cid: str
    spotify_pwd: str
    db_host: str
    db_name: str
    db_username: str
    db_password: str

    # for migration
    input_path: str = "input/migration"
    pl_file: str = "playlists_0721.csv"
    song_file: str = "join_songs_0726_unique.csv"

    # for output crawled csv
    enable_output_csv: bool = False
    output_path: str = "output/crawler"
    output_pl_file: str = "playlists_1014.csv"

    class Config:
        env_file = ".env"
