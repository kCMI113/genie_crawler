import unittest
from .common import connect_to_db
import db
from dto.model import Artist
from db.repository import ArtistRepository
from db.exception import NotFoundArtistException
from datetime import datetime, timedelta
import time


class TestArtist(unittest.TestCase):
    artist_repository = ArtistRepository()

    @classmethod
    def setUp(cls):
        connect_to_db()

    @classmethod
    def tearDown(cls):
        db.disconnect()

    def test_create_artist(self):
        self.__artist("H1", "주혜인")

    def test_delete_by_genie_id(self):
        artist = self.__artist("H1", "주혜인")

        self.artist_repository.delete_by_genie_id(artist.genie_id)
        found = self.artist_repository.find_by_genie_id(artist.genie_id)
        assert found is None

        # not exists playlist
        self.assertRaises(
            NotFoundArtistException,
            lambda: self.artist_repository.delete_by_genie_id(artist.genie_id),
        )

    def test_find_by_geine_id(self):
        artist = self.__artist("H1", "주혜인")

        found = self.artist_repository.find_by_genie_id(artist.genie_id)
        assert artist == found

    def test_find_by_updated_at_gte(self):
        artist1 = self.__artist("H1", "주혜인")
        time.sleep(0.01)
        artist2 = self.__artist("H2", "박동연")

        found = self.artist_repository.find_by_updated_at_gte(datetime.utcnow() - timedelta(milliseconds=1))
        assert [artist2] == found

    def test_find_all(self):
        artists = [self.__artist("H1", "주혜인"), self.__artist("H2", "박동연"), self.__artist("H3", "강찬미")]

        found = self.artist_repository.find_all()
        assert artists == found

    def __artist(self, genie_id: str, name: str) -> Artist:
        return self.artist_repository.create_artist(genie_id, name)
