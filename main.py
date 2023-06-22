import hydra
import pandas as pd
from tqdm import tqdm
from omegaconf import DictConfig

from selenium.common.exceptions import UnexpectedAlertPresentException

from src.utils import setLogFile, getLastPlaylistId, saveInfoDict2Csv
from src.crawler import getPlaylistInfo


@hydra.main(version_base="1.2", config_path="configs", config_name="config.yaml")
def main(config: DictConfig = None) -> None:
    setting = config

    # log file setting
    filename = setLogFile(setting)
    f = open(filename, "w")

    # get last playlist id
    print("---------- Check Last playlist item id ... ----------")
    last_pl_id = getLastPlaylistId(setting.playlist_origin_url)
    f.write(f"[NOTICE] Last playlist item id is {last_pl_id} !!!\n")
    print(f"[NOTICE] Last playlist item id is {last_pl_id} !!!")

    # crawling playlists and songs
    print("---------- Start playlist crawling ... ----------")
    pl_list, songs_list = [], []

    for id in tqdm(range(setting.start_idx, setting.end_idx + 1)):
        try:
            pl_url = setting.playlist_url + str(id)
            pl_info = getPlaylistInfo(pl_url, setting, songs_list)
            pl_list.append(pl_info)
            f.write(f"playlist {id} is saved ...\n")
        except UnexpectedAlertPresentException:
            f.write(f">>> >>> Cannot find playlist {id} !!!\n")
            print(f">>> >>> Cannot find playlist {id} !!!")
        except Exception as ex:
            f.write(f">>> >>> {ex} : Error is occured at id {id} !!!\n")
            print(f">>> >>> {ex} : Error is occured at id {id} !!!")
            exit()

    f.close()

    # save crwaling results
    saveInfoDict2Csv(pl_list, songs_list, setting)


if __name__ == "__main__":
    main()
