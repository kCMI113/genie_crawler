import pandas as pd
from db.repository import SongRepository, PlaylistRepository
from dto.model import Song


class PlaylistCsvMigrate:
    def __init__(path: str):
        df = pd.read_csv(path)
        song_repository = SongRepository()
        playlist_repository = PlaylistRepository()

    def find_songs(self, genie_ids: list[str]) -> list[Song]:
        # 지니아이디 리스트로 들어오면 들어온 노래 찾아서 list[doc]으로 내보내기
        return

    def add_playlists(self) -> None:
        # 플리 지니아이디(genie_ids:list[str]) 얻어서 그걸로 반복문 돌기
        # find_songs(ids)
        # playlist doc create
        return
