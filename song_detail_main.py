import hydra
import pandas as pd
from tqdm import tqdm
from omegaconf import DictConfig
import os

from src.utils import setLogFile
from src.song_detail_crawler import crawlSongDetail


@hydra.main(version_base="1.2", config_path="configs", config_name="song_detail.yaml")
def main(config: DictConfig = None) -> None:
    # log file setting
    filename = setLogFile(config)
    logger = open(filename, "w")

    # load base song info
    print("---------- Load song_info files to retrieve song_id ----------")
    song_info_path = os.path.join(config.out_dir, config.song_info_filename)
    song_info_df = pd.read_csv(song_info_path, dtype={"SONG_ID": int})
    song_ids: list[int] = song_info_df["SONG_ID"].to_list()

    # crawling playlists and songs
    print("---------- Start song detail crawling ... ----------")
    sond_details = []
    for song_id in tqdm(song_ids):
        song_detail = crawlSongDetail(song_id, config.song_detail_url)
        print(song_detail)
        sond_details.append(song_detail)

    logger.close()

    # save crwaling results
    # TODO


if __name__ == "__main__":
    main()
