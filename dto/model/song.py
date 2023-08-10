from pydantic import BaseModel
from .artist import Artist
from .album import Album
from datetime import datetime


class Song(BaseModel):
    id: str
    genie_id: str
    title: str
    lyrics: str
    album: Album
    artist: Artist
    like_cnt: int
    listener_cnt: int
    play_cnt: int
    genres: list[str]
    spotify_url: str | None
    created_at: datetime
    updated_at: datetime
