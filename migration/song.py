import pandas as pd
from db.repository import (
    AlbumRepository,
    SongRepository,
    ArtistRepository,
)
from dto.model import Album, Artist
from tqdm import tqdm


class SongCsvMigrate:
    def __init__(self, path: str):
        self.df = pd.read_csv(path)
        self.album_repository = AlbumRepository()
        self.artist_repository = ArtistRepository()
        self.song_repository = SongRepository()

    def add_albums(self) -> None:
        print("##### MIGRATING ALBUM TO DB #####")
        album_df = self.df[["ALBUM_TITLE", "ALBUM_ID", "IMG_PATH", "RELEASE_DATE"]]

        for idx in tqdm(range(0, len(album_df))):
            name = album_df.iloc[idx]["ALBUM_TITLE"]
            id = str(album_df.iloc[idx]["ALBUM_ID"])
            img_url = album_df.iloc[idx]["IMG_PATH"]
            released_date = album_df.iloc[idx]["RELEASE_DATE"]

            if not self.album_repository.find_by_genie_id(id):
                self.album_repository.create_Album(id, name, img_url, released_date)

    def find_album(self, genie_id: str) -> Album:
        return

    def add_artists(self) -> None:
        print("##### MIGRATING ARTIST TO DB #####")
        artist_df = self.df[["ARTIST_NAME", "ARTIST_ID"]]

        for idx in tqdm(range(0, len(artist_df))):
            name = artist_df.iloc[idx]["ARTIST_NAME"]
            id = str(artist_df.iloc[idx]["ARTIST_ID"])

            if not self.artist_repository.find_by_genie_id(id):
                self.artist_repository.create_artist(id, name)

    def find_artist(self, genie_id: str) -> Artist:
        # 지니아이디로 쿼리(지니아이디)로 들어온 아티스트 도쿠먼트 찾아서 보내기
        return

    def add_songs(self):
        # 송 지니아이디(genie_ids:list[str]) 얻어서 그걸로 반복문 돌기
        # find_artist(id)
        # find_album(id)
        # song doc create
        return
