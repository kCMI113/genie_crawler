import hydra
import pandas as pd
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
from omegaconf import DictConfig
import os

from ..utils import getLogger
from .song.song_detail_crawler import crawlSongDetail


@hydra.main(version_base="1.2", config_path="configs", config_name="song.yaml")
def main(config: DictConfig = None) -> None:
    # log file setting
    log = getLogger()
    log.propagate = False

    # load base song info
    song_info_path = os.path.join(config.out_dir, config.song_info_filename)
    log.info("Load song_info files to retrieve song_id from %s", song_info_path)
    song_info_df = pd.read_csv(song_info_path, dtype={"SONG_ID": int})
    song_ids: list[int] = song_info_df["SONG_ID"].to_list()

    # crawling playlists and songs
    log.info("Start song detail crawling ...")
    song_details = []
    failed_crawling_song_ids = []
    for song_id in tqdm(song_ids, position=0, leave=True):
        with logging_redirect_tqdm():
            try:
                song_detail = crawlSongDetail(song_id, config.song_detail_url, log)
                song_details.append(song_detail)
            except Exception as e:
                log.exception(e)
                failed_crawling_song_ids.append(song_id)

    if failed_crawling_song_ids:
        log.warn("Failed crawling song ids : %s", str(failed_crawling_song_ids))

    # save crwaling results
    csv_path = os.path.join(config.out_dir, config.song_detail_filename)
    log.info("Save concatencated song_info to %s", csv_path)
    song_details_df = pd.DataFrame(song_details)
    song_details_df.to_csv(csv_path)


if __name__ == "__main__":
    main()
