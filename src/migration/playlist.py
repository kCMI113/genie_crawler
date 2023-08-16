import pandas as pd
from src.db import SongRepository, PlaylistRepository, Song
from tqdm import tqdm
import ast


class PlaylistCsvMigrate:
    def __init__(self, path: str):
        self.df = pd.read_csv(path, dtype={"playlist_id": str})
        self.song_repository = SongRepository()
        self.playlist_repository = PlaylistRepository()

    def find_song_docs(self, genie_ids: list[str]) -> list[Song]:
        songs = []
        for genie_id in genie_ids:
            song = self.song_repository.find_by_genie_id(genie_id)
            if song:
                songs.append(song)

        return songs

    def add_playlists(self) -> None:
        print("##### MIGRATING PLAYLIST TO DB #####")
        pl_df = self.df

        for idx in tqdm(range(0, len(pl_df))):
            id = pl_df.iloc[idx]["playlist_id"]

            if not self.playlist_repository.find_by_genie_id(id):
                title = pl_df.iloc[idx]["playlist_title"]
                subtitle = pl_df.iloc[idx]["playlist_subtitle"]
                like_cnt = pl_df.iloc[idx]["playlist_likecount"]
                view_cnt = pl_df.iloc[idx]["playlist_view"]
                tags = ast.literal_eval(pl_df.iloc[idx]["playlist_tags"])
                img_url = pl_df.iloc[idx]["playlist_img_url"]
                songs = self.find_song_docs(ast.literal_eval(pl_df.iloc[idx]["playlist_songs"]))
                song_cnt = len(songs)

                if song_cnt:
                    self.playlist_repository.create_playlist(id, title, subtitle, song_cnt, like_cnt, view_cnt, tags, songs, img_url)
