import unittest
from datetime import date, datetime, timedelta
import db
from .common import connect_to_db
from db.repository import PlaylistRepository, SongRepository, ArtistRepository, AlbumRepository
from db.exception import (
    NotFoundPlaylistException,
    NotFoundSongException,
)
from dto.model import Playlist, Song, Artist, Album
import time


class TestPlaylist(unittest.TestCase):
    song_repository = SongRepository()
    playlist_repository = PlaylistRepository()
    artist_repository = ArtistRepository()
    album_repository = AlbumRepository()

    @classmethod
    def setUp(cls):
        connect_to_db()

    @classmethod
    def tearDown(cls):
        db.disconnect()

    def test_create_playlist(self):
        artist = self.__artist()
        album = self.__album()
        song = self.__song(artist=artist, album=album, genie_id="S1")
        self.__playlist(songs=[song], genie_id="1")

        # not exists song
        fake_song = Song(
            id="1234",
            genie_id="S3",
            title="title",
            lyrics="lyrics",
            album=album,
            artist=artist,
            like_cnt=10,
            listener_cnt=1,
            play_cnt=1,
            genres=["genres"],
            created_at=date(2000, 3, 15),
            updated_at=date(2000, 3, 15),
            spotify_url=None,
        )
        self.assertRaises(NotFoundSongException, lambda: self.__playlist(songs=[fake_song], genie_id="2"))

    def test_delete_by_genie_id(self):
        artist = self.__artist()
        album = self.__album()
        song = self.__song(artist=artist, album=album)
        playlist = self.__playlist(songs=[song])

        self.playlist_repository.delete_by_genie_id(playlist.genie_id)
        found = self.playlist_repository.find_by_genie_id(playlist.genie_id)
        assert found is None

        # not exists playlist
        self.assertRaises(
            NotFoundPlaylistException,
            lambda: self.playlist_repository.delete_by_genie_id(playlist.genie_id),
        )

    def test_find_by_geine_id(self):
        artist = self.__artist()
        album = self.__album()
        song = self.__song(artist=artist, album=album)
        playlist = self.__playlist(songs=[song])

        found = self.playlist_repository.find_by_genie_id(playlist.genie_id)
        assert playlist == found

    def test_find_by_updated_at_gte(self):
        artist = self.__artist()
        album = self.__album()
        song = self.__song(artist=artist, album=album)

        playlist1 = self.__playlist(songs=[song], genie_id="P1")
        time.sleep(0.01)
        playlist2 = self.__playlist(songs=[song], genie_id="P2")

        found = self.playlist_repository.find_by_updated_at_gte(datetime.utcnow() - timedelta(milliseconds=1))
        assert [playlist2] == found

    def test_find_all(self):
        artist = self.__artist()
        album = self.__album()
        song = self.__song(artist=artist, album=album)

        playlists = [
            self.__playlist(songs=[song], genie_id="P1"),
            self.__playlist(songs=[song], genie_id="P2"),
            self.__playlist(songs=[song], genie_id="P3"),
        ]

        found = self.playlist_repository.find_all()
        assert playlists == found

    def __song(
        self,
        album: Album,
        artist: Artist,
        genie_id: str = "S1",
        title: str = "노래",
        lyrics: str = "사가",
        like_cnt: int = 10,
        listener_cnt: int = 1,
        play_cnt: int = 2,
        genres: list[str] = ["락"],
        spotify_url: str = "http://song.mp4",
    ) -> Song:
        return self.song_repository.create_song(genie_id, title, lyrics, album, artist, like_cnt, listener_cnt, play_cnt, genres, spotify_url)

    def __artist(self, genie_id: str = "A1", name: str = "주혜인") -> Artist:
        return self.artist_repository.create_artist(genie_id, name)

    def __album(self, genie_id: str = "M1", name: str = "주혜아웃", img_url: str = "http://album.png", released_date: date = date(2000, 3, 15)) -> Album:
        return self.album_repository.create_Album(genie_id, name, img_url, released_date)

    def __playlist(
        self,
        songs: list[Song],
        genie_id: str = "P1",
        title: str = "주혜인의 플리",
        subtitle: str = "나 주혜인이 푸른 달이 뜨는 밤.. 방구석에서 몰래 듣는 노래를 모아봄",
        song_cnt: int = 1,
        like_cnt: int = 10,
        view_cnt: int = 20,
        tags: list[str] = ["tag"],
        img_url: str = "http://pl.png",
    ) -> Playlist:
        return self.playlist_repository.create_playlist(genie_id, title, subtitle, song_cnt, like_cnt, view_cnt, tags, songs, img_url)
