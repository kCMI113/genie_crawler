import pandas as pd
from db.repository import (
    AlbumRepository,
    SongRepository,
    ArtistRepository,
)
from dto.model import Album, Artist


class SongCsvMigrate:
    def __init__(path: str):
        df = pd.read_csv(path)
        album_repository = AlbumRepository()
        artist_repository = ArtistRepository()
        song_repository = SongRepository()

    def add_albums(self) -> None:
        # df에서 앨범관련 컬럼만 살려서 반복문 돌며 디비에 넣기
        return 0

    def find_album(self, genie_id: str) -> Album:
        # 지니아이디로 쿼리(지니아이디)로 들어온 앨범 도쿠먼트 찾아서 보내기
        return

    def add_artists(self) -> None:
        # df에서 아티스트 관련 컬럼만 살려서 반복문 돌며 디비에 넣기
        return 0

    def find_artist(self, genie_id: str) -> Artist:
        # 지니아이디로 쿼리(지니아이디)로 들어온 아티스트 도쿠먼트 찾아서 보내기
        return

    def add_songs(self):
        # 송 지니아이디(genie_ids:list[str]) 얻어서 그걸로 반복문 돌기
        # find_artist(id)
        # find_album(id)
        # song doc create
        return
