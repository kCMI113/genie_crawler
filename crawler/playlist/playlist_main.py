import hydra
import pandas as pd
from tqdm import tqdm
from omegaconf import DictConfig

from selenium.common.exceptions import UnexpectedAlertPresentException

from ..utils import getLogger, getLastPlaylistId, saveInfoDict2Csv
from .playlist_crawler import getPlaylistInfo


@hydra.main(version_base="1.2", config_path="configs", config_name="playlist.yaml")
def main(config: DictConfig = None) -> None:
    setting = config

    # logger setting
    log = getLogger()
    log.propagate = False

    # crawling playlists and songs
    log.info("Start playlist crawling ...")
    pl_list, songs_list = [], []

    # set searching playlist idx
    start_idx = setting.start_idx
    if setting.end_idx:
        end_idx = setting.end_idx
    else:
        # get last playlist id
        log.info("Check Last playlist item id ...")
        end_idx = getLastPlaylistId(setting.playlist_origin_url)
        log.info("-- Last playlist item id is %d !!!", end_idx)
    err_list = []

    # start searching
    for id in tqdm(range(start_idx, end_idx + 1)):
        try:
            pl_url = setting.playlist_url + str(id)
            pl_info = getPlaylistInfo(id=id, link=pl_url, setting=setting, songs_list=songs_list, logger=log)
            pl_list.append(pl_info)
            log.info("playlist Id: %d", id)
        except UnexpectedAlertPresentException:
            log.warning("Cannot find playlist %d", id)
        except Exception as ex:
            err_list.append(id)
            log.warning("%s : Error is occured at id %d", ex, id)

    # save crwaling results
    saveInfoDict2Csv(pl_list=pl_list, songs_list=songs_list, setting=setting, start_idx=start_idx, end_idx=end_idx)
    log.info("err_index: %s", err_list)


if __name__ == "__main__":
    main()
