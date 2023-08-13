import pandas as pd
from db.repository import (
    AlbumRepository,
    SongRepository,
    ArtistRepository,
)
from tqdm import tqdm
from spotify.spotify import get_spotify_url


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

    def add_artists(self) -> None:
        print("##### MIGRATING ARTIST TO DB #####")
        artist_df = self.df[["ARTIST_NAME", "ARTIST_ID"]]

        for idx in tqdm(range(0, len(artist_df))):
            name = artist_df.iloc[idx]["ARTIST_NAME"]
            id = str(artist_df.iloc[idx]["ARTIST_ID"])

            if not self.artist_repository.find_by_genie_id(id):
                self.artist_repository.create_artist(id, name)

    def add_songs(self):
        print("##### MIGRATING SONG TO DB #####")
        song_df = self.df

        for idx in tqdm(range(0, len(song_df))):
            title = song_df.iloc[idx]["SONG_TITLE"]
            id = str(song_df.iloc[idx]["ARTIST_ID"])
            lyrics = song_df.iloc[idx]["LYRICS"]
            listener_cnt = song_df.iloc[idx]["LISTENER_CNT"]
            like_cnt = song_df.iloc[idx]["SONG_LIKE"]
            play_cnt = song_df.iloc[idx]["PLAY_CNT"]
            genres = song_df.iloc[idx]["INFO_GENRE"].replace(" ", "").split("/")
            artist = self.artist_repository.find_by_genie_id(str(song_df.iloc[idx]["ARTIST_ID"]))
            album = self.album_repository.find_by_genie_id(str(song_df.iloc[idx]["ALBUM_ID"]))
            spotify_url = get_spotify_url(title, artist.name, album.released_date)

            if not self.song_repository.find_by_genie_id(id):
                self.song_repository.create_song(id, title, lyrics, album, artist, like_cnt, listener_cnt, play_cnt, genres, spotify_url)
