import os
import db
import pandas as pd
from config.config import DBConfig
from migration.crawler import CrawlerMigrate
from crawler.album_main import crawlAlbum
from crawler.song_main import crawlSong
from crawler.playlist_main import crawlPlaylist

config = DBConfig()
PLAYLIST_PATH = os.path.join(config.input_path, config.pl_file)
SONG_PATH = os.path.join(config.input_path, config.song_file)


def main() -> None:
    db.connect(config.db_name, config.db_host, config.db_username, config.db_password)

    pl_df, song_df = crawlPlaylist()
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
