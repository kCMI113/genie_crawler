import os
import pandas as pd
from src.config import DBConfig, GenieConfig
from src.db import db, PlaylistRepository
from src.migration import CrawlerMigrate
from src.crawler import crawlAlbum, crawlPlaylist, crawlSong


config = DBConfig()
genie_config = GenieConfig()
PLAYLIST_PATH = os.path.join(config.input_path, config.pl_file)
SONG_PATH = os.path.join(config.input_path, config.song_file)


def main() -> None:
    db.connect(config.db_name, config.db_host, config.db_username, config.db_password)

    if config.use_latest_start_idx:
        genie_config.start_idx = int(PlaylistRepository().find_latest_created_playlist().genie_id) + 1
        print(f"start_idx: {genie_config.start_idx}")

    pl_df, song_df = crawlPlaylist(genie_config)
    song_df = pd.merge(song_df, crawlSong(list(song_df["SONG_ID"])), on="SONG_ID", how="inner")
    song_df = pd.merge(song_df, crawlAlbum(list(song_df["ALBUM_ID"])), on="ALBUM_ID", how="inner")

    crawler_migrate = CrawlerMigrate(song_df, pl_df)

    crawler_migrate.add_albums()
    crawler_migrate.add_artists()
    crawler_migrate.add_songs()
    crawler_migrate.add_playlists()

    db.disconnect()


if __name__ == "__main__":
    main()
