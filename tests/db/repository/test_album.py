import unittest
from .common import connect_to_db
import db
from dto.model import Album
from db.repository import AlbumRepository
from db.exception import NotFoundAlbumException
from datetime import date, datetime


class Testalbum(unittest.TestCase):
    albumRepository = AlbumRepository()

    @classmethod
    def setUp(cls):
        connect_to_db()

    @classmethod
    def tearDown(cls):
        db.disconnect()

    def test_create_album(self):
        self.__album(
            "H1",
            "주혜인",
            "http://album.png",
            date(2001, 3, 13),
        )

    def test_delete_by_genie_id(self):
        album = self.__album(
            "H1",
            "주혜인",
            "http://album.png",
            date(2001, 3, 13),
        )

        self.albumRepository.delete_by_genie_id(album.genie_id)
        found = self.albumRepository.find_by_genie_id(album.genie_id)
        assert found is None

        # not exists playlist
        self.assertRaises(
            NotFoundAlbumException,
            lambda: self.albumRepository.delete_by_genie_id(album.genie_id),
        )

    def test_find_by_geine_id(self):
        album = self.__album(
            "H1",
            "주혜인",
            "http://album.png",
            date(2001, 3, 13),
        )

        found = self.albumRepository.find_by_genie_id(album.genie_id)
        assert album == found

    def test_find_by_updated_at_gte(self):
        album = self.__album(
            "H1",
            "주혜인",
            "http://album.png",
            date(2001, 3, 13),
        )

        found = self.albumRepository.find_by_updated_at_gte(datetime(2023, 8, 9, 21, 12, 21))
        assert album == found

    def test_find_all(self):
        album1 = self.__album(
            "H1",
            "주혜인",
            "http://album.png",
            date(2001, 3, 13),
        )
        album2 = self.__album(
            "H2",
            "서민석",
            "http://album.png",
            date(2005, 12, 8),
        )
        album3 = self.__album(
            "H3",
            "이준영",
            "http://album.png",
            date(2000, 3, 15),
        )

        found = self.albumRepository.find_all()
        for album in [album1, album2, album3]:
            assert album in found

    def __album(self, genie_id: str, name: str, img_url: str, released_date: date) -> Album:
        return self.albumRepository.create_Album(genie_id, name, img_url, released_date)
