from ..document import PlaylistDocument
from ..exception import NotFoundPlaylistException
from ...dto.model import Playlist, Song
from .common import find_song_docs_by_dto
from datetime import datetime
from mongoengine import QuerySet


class PlaylistRepository:
    def create_playlist(
        self,
        genie_id: str,
        title: str,
        subtitle: str,
        song_cnt: int,
        like_cnt: int,
        view_cnt: int,
        tags: list[str],
        songs: list[Song],
        img_url: str,
    ) -> Playlist:
        song_docs = find_song_docs_by_dto(songs)
        playlist = PlaylistDocument(
            genie_id=genie_id,
            title=title,
            subtitle=subtitle,
            song_cnt=song_cnt,
            like_cnt=like_cnt,
            view_cnt=view_cnt,
            tags=tags,
            songs=song_docs,
            img_url=img_url,
        )
        saved: PlaylistDocument = playlist.save()
        return saved.to_dto()

    def delete_by_genie_id(self, genie_id: str) -> None:
        playlist: PlaylistDocument = PlaylistDocument.objects(genie_id=genie_id).first()

        if not playlist:
            raise NotFoundPlaylistException(f"Can't find playlist document: genie_id={genie_id}")

        playlist.delete()

    def find_by_genie_id(self, genie_id: str) -> Playlist:
        playlist: PlaylistDocument = PlaylistDocument.objects(genie_id=genie_id).first()

        if not playlist:
            return None

        return playlist.to_dto()

    def find_by_updated_at_gte(self, query_dt: datetime) -> list[Playlist]:
        playlists: QuerySet[PlaylistDocument] = PlaylistDocument.objects(upated_at__gte=query_dt)

        if not playlists:
            return None

        return [playlist.to_dto() for playlist in playlists]

    def find_all(self) -> list[Playlist]:
        playlists: QuerySet[PlaylistDocument] = PlaylistDocument.objects
        return [playlist.to_dto() for playlist in playlists]
