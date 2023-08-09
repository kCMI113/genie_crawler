from ..document import InferenceDocument, SongsElementEmbeddedDocument
from ...dto.model import Inference, SongsElement, User, Playlist
from .common import find_song_doc_by_dto, find_user_doc_by_dto, find_playlist_docs_by_dto
from datetime import datetime
from mongoengine import QuerySet


def songs_element_dto2embedded_doc(song_el: SongsElement) -> SongsElementEmbeddedDocument:
    song_doc = find_song_doc_by_dto(song_el.song)
    return SongsElementEmbeddedDocument(song=song_doc, is_like=song_el.is_like)


class InferenceRepository:
    def create_inference(
        self, user: User, query_img_url: str, playlists: list[Playlist], songs: list[SongsElement], genres: list[str], created_at: datetime
    ) -> Inference:
        user_doc = find_user_doc_by_dto(user)
        playlist_docs = find_playlist_docs_by_dto(playlists)
        song_docs = [songs_element_dto2embedded_doc(song) for song in songs]

        inference = InferenceDocument(
            user=user_doc,
            query_img_url=query_img_url,
            playlists=playlist_docs,
            songs=song_docs,
            genres=genres,
            created_at=created_at,
            updated_at=created_at,
        )
        saved: InferenceDocument = inference.save()
        return saved.to_dto()

    def find_by_updated_at_gte(self, query_dt: datetime) -> list[Inference]:
        Inferences: QuerySet[InferenceDocument] = InferenceDocument.objects(upated_at__gte=query_dt)

        if not Inferences:
            return None

        return [Inference.to_dto() for Inference in Inferences]

    def find_all(self) -> list[Inference]:
        inferences: QuerySet[InferenceDocument] = InferenceDocument.objects
        return [inference.to_dto() for inference in inferences]
