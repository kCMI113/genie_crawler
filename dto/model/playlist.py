from pydantic import BaseModel
from datetime import datetime
from .song import Song


class Playlist(BaseModel):
    id: str
    genie_id: str
    title: str
    subtitle: str
    song_cnt: int
    like_cnt: int
    view_cnt: int
    tags: list[str]
    songs: list[Song]
    img_url: str
    created_at: datetime
    updated_at: datetime
