import unittest
from datetime import date, datetime, timedelta
import db
from .common import connect_to_db
from db.repository import (
    AlbumRepository,
    SongRepository,
    ArtistRepository,
)
from db.exception import (
    NotFoundAlbumException,
    NotFoundSongException,
    NotFoundArtistException,
)
from dto.model import Album, Artist, Song


class TestSong(unittest.TestCase):
    songRepository = SongRepository()
    artistRepository = ArtistRepository()
    albumRepository = AlbumRepository()

    @classmethod
    def setUp(cls):
        connect_to_db()

    @classmethod
    def tearDown(cls):
        db.disconnect()

    def test_create_song(self):
        artist = self.__artist()
        album = self.__album()
        self.__song(artist=artist, album=album, genie_id="S1")

        # not exists artist
        fake_artist = Artist(id="123", genie_id="A3", name="없는것", created_at=date(2000, 3, 15), updated_at=date(2000, 3, 15))
        fake_album = Album(
            id="456",
            genie_id="A9",
            name="없다",
            img_url="http://album.png",
            released_date=date(2000, 3, 15),
            created_at=date(2000, 3, 15),
            updated_at=date(2000, 3, 15),
        )
        self.assertRaises(NotFoundArtistException, lambda: self.__song(artist=fake_artist, album=album, genie_id="S2"))
        self.assertRaises(NotFoundAlbumException, lambda: self.__song(artist=artist, album=fake_album, genie_id="E1"))

    def test_delete_by_genie_id(self):
        artist = self.__artist()
        album = self.__album()
        song = self.__song(artist=artist, album=album)

        self.songRepository.delete_by_genie_id(song.genie_id)
        found = self.songRepository.find_by_genie_id(song.genie_id)
        assert found is None

        # not exists song
        self.assertRaises(
            NotFoundSongException,
            lambda: self.songRepository.delete_by_genie_id(song.genie_id),
        )

    def test_find_by_geine_id(self):
        artist = self.__artist()
        album = self.__album()
        song = self.__song(artist=artist, album=album)

        found = self.songRepository.find_by_genie_id(song.genie_id)
        assert song == found

    def test_find_by_updated_at_gte(self):
        artist = self.__artist()
        album = self.__album()
        songs = [
            self.__song(artist=artist, album=album, genie_id="S1"),
            self.__song(artist=artist, album=album, genie_id="S2"),
            self.__song(artist=artist, album=album, genie_id="S3"),
        ]

        found = self.songRepository.find_by_updated_at_gte(datetime.now() - timedelta(days=1))
        assert songs == found

    def test_find_all(self):
        artist = self.__artist()
        album = self.__album()
        songs = [
            self.__song(artist=artist, album=album, genie_id="S1"),
            self.__song(artist=artist, album=album, genie_id="S2"),
            self.__song(artist=artist, album=album, genie_id="S3"),
        ]

        found = self.songRepository.find_all()
        for song in songs:
            assert song in found

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
        return self.songRepository.create_song(genie_id, title, lyrics, album, artist, like_cnt, listener_cnt, play_cnt, genres, spotify_url)

    def __artist(self, genie_id: str = "A1", name: str = "주혜인") -> Artist:
        return self.artistRepository.create_artist(genie_id, name)

    def __album(self, genie_id: str = "H1", name: str = "주혜아웃", img_url: str = "http://album.png", released_date: date = date(2000, 3, 15)) -> Album:
        return self.albumRepository.create_Album(genie_id, name, img_url, released_date)
