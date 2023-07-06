import hydra
import pandas as pd
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
from omegaconf import DictConfig
import os

from src.utils import getLogger
from src.song_detail_crawler import crawlSongDetail


@hydra.main(version_base="1.2", config_path="configs", config_name="song_detail.yaml")
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
    for song_id in tqdm(song_ids, position=0, leave=True):
        with logging_redirect_tqdm():
            try:
                song_detail = crawlSongDetail(song_id, config.song_detail_url, log)
                song_details.append(song_detail)
            except Exception as e:
                log.exception(e)
    # save crwaling results
    csv_path = os.path.join(config.out_dir, config.song_detail_filename)
    log.info("Save concatencated song_info to %s", csv_path)
    song_details_df = pd.DataFrame(song_details)
    concatenated_df = song_details_df.set_index("SONG_ID").join(song_info_df.set_index("SONG_ID"), on="SONG_ID", how="left")
    concatenated_df.to_csv(csv_path)


if __name__ == "__main__":
    main()
