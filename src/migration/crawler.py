import pandas as pd
from ..db import SongRepository, PlaylistRepository, AlbumRepository, ArtistRepository, Song
from tqdm import tqdm
from .spotify import getSpotifyUrl


class CrawlerMigrate:
    def __init__(self, song_df: pd.DataFrame, pl_df: pd.DataFrame):
        self.song_df = song_df.drop_duplicates("SONG_ID")
        self.pl_df = pl_df
        self.album_repository = AlbumRepository()
        self.artist_repository = ArtistRepository()
        self.song_repository = SongRepository()
        self.playlist_repository = PlaylistRepository()

    def add_albums(self) -> None:
        print("##### MIGRATING ALBUM TO DB #####")
        album_df = self.song_df[["ALBUM_TITLE", "ALBUM_ID", "IMG_PATH", "RELEASE_DATE"]]

        for idx in tqdm(range(len(album_df))):
            id = album_df.iloc[idx]["ALBUM_ID"]

            if not self.album_repository.find_by_genie_id(id):
                name = album_df.iloc[idx]["ALBUM_TITLE"]
                img_url = album_df.iloc[idx]["IMG_PATH"]
                released_date = album_df.iloc[idx]["RELEASE_DATE"]

                self.album_repository.create_Album(id, name, img_url, released_date)

    def add_artists(self) -> None:
        print("##### MIGRATING ARTIST TO DB #####")
        artist_df = self.song_df[["ARTIST_NAME", "ARTIST_ID"]]

        for idx in tqdm(range(len(artist_df))):
            id = artist_df.iloc[idx]["ARTIST_ID"]

            if not self.artist_repository.find_by_genie_id(id):
                name = artist_df.iloc[idx]["ARTIST_NAME"]

                self.artist_repository.create_artist(id, name)

    def add_songs(self):
        print("##### MIGRATING SONG TO DB #####")

        for idx in tqdm(range(len(self.song_df))):
            id = self.song_df.iloc[idx]["SONG_ID"]

            if not self.song_repository.find_by_genie_id(id):
                title = self.song_df.iloc[idx]["SONG_TITLE"]
                lyrics = str(self.song_df.iloc[idx]["LYRICS"])
                listener_cnt = self.song_df.iloc[idx]["LISTENER_CNT"]
                like_cnt = self.song_df.iloc[idx]["SONG_LIKE"]
                play_cnt = self.song_df.iloc[idx]["PLAY_CNT"]
                genres = self.song_df.iloc[idx]["INFO_GENRE"].replace(" ", "").split("/")
                artist = self.artist_repository.find_by_genie_id(str(self.song_df.iloc[idx]["ARTIST_ID"]))
                album = self.album_repository.find_by_genie_id(str(self.song_df.iloc[idx]["ALBUM_ID"]))
                spotify_url = getSpotifyUrl(title, artist.name, album.released_date)

                self.song_repository.create_song(id, title, lyrics, album, artist, like_cnt, listener_cnt, play_cnt, genres, spotify_url)

    def find_song_docs(self, genie_ids: list[str]) -> list[Song]:
        songs = []
        for genie_id in genie_ids:
            song = self.song_repository.find_by_genie_id(genie_id)
            if song:
                songs.append(song)

        return songs

    def add_playlists(self) -> None:
        print("##### MIGRATING PLAYLIST TO DB #####")

        for idx in tqdm(range(len(self.pl_df))):
            id = self.pl_df.iloc[idx]["PLAYLIST_ID"]

            if not self.playlist_repository.find_by_genie_id(id):
                title = self.pl_df.iloc[idx]["PLAYLIST_TITLE"]
                subtitle = self.pl_df.iloc[idx]["PLAYLIST_SUBTITLE"]
                like_cnt = self.pl_df.iloc[idx]["PLAYLIST_LIKECOUNT"]
                view_cnt = self.pl_df.iloc[idx]["PLAYLIST_VIEW"]
                tags = self.pl_df.iloc[idx]["PLAYLIST_TAGS"]
                img_url = self.pl_df.iloc[idx]["PLAYLIST_IMG_URL"]
                songs = self.find_song_docs(self.pl_df.iloc[idx]["PLAYLIST_SONGS"])
                song_cnt = len(songs)

                if song_cnt:
                    self.playlist_repository.create_playlist(id, title, subtitle, song_cnt, like_cnt, view_cnt, tags, songs, img_url)
