from ..document import SongDocument
from dto.model import Album, Artist, Song
from ..exception import NotFoundSongException
from .common import find_album_doc_by_dto, find_artist_doc_by_dto
from datetime import datetime
from mongoengine import QuerySet


class SongRepository:
    def create_song(
        self,
        genie_id: str,
        title: str,
        lyrics: str,
        album: Album,
        artist: Artist,
        like_cnt: int,
        listener_cnt: int,
        play_cnt: int,
        genres: list[str],
        spotify_url: str,
    ) -> Song:
        song = SongDocument(
            genie_id=genie_id,
            title=title,
            lyrics=lyrics,
            album=find_album_doc_by_dto(album),
            artist=find_artist_doc_by_dto(artist),
            like_cnt=like_cnt,
            listener_cnt=listener_cnt,
            play_cnt=play_cnt,
            genres=genres,
            spotify_url=spotify_url,
        )
        saved: SongDocument = song.save()
        return saved.to_dto()

    def delete_by_genie_id(self, genie_id: str) -> None:
        song: SongDocument = SongDocument.objects(genie_id=genie_id).first()

        if not song:
            raise NotFoundSongException(f"Can't find song document: genie_id={genie_id}")

        song.delete()

    def find_by_genie_id(self, genie_id: str) -> Song | None:
        song: SongDocument = SongDocument.objects(genie_id=genie_id).first()

        if not song:
            return None

        return song.to_dto()

    def find_by_updated_at_gte(self, query_dt: datetime) -> list[Song]:
        songs: QuerySet[SongDocument] = SongDocument.objects(updated_at__gte=query_dt)

        if not songs:
            return None

        return [song.to_dto() for song in songs]

    def find_all(self) -> list[Song]:
        songs: QuerySet[SongDocument] = SongDocument.objects
        return [song.to_dto() for song in songs]
