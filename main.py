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

    # crawling playlists and songs
    print("---------- Start playlist crawling ... ----------")
    pl_list, songs_list = [], []

    # set searching playlist idx
    start_idx = setting.start_idx
    if setting.end_idx:
        end_idx = setting.end_idx
    else:
        # get last playlist id
        print("---------- Check Last playlist item id ... ----------")
        end_idx = getLastPlaylistId(setting.playlist_origin_url)
        f.write(f"[NOTICE] Last playlist item id is {end_idx} !!!\n")
        print(f"[NOTICE] Last playlist item id is {end_idx} !!!")
    err_list = []
    # start searching
    for id in tqdm(range(start_idx, end_idx + 1)):
        try:
            pl_url = setting.playlist_url + str(id)
            pl_info = getPlaylistInfo(id=id, link=pl_url, setting=setting, songs_list=songs_list)
            pl_list.append(pl_info)
            f.write(f"playlist {id} is saved ...\n")
        except UnexpectedAlertPresentException:
            f.write(f">>> >>> Cannot find playlist {id} !!!\n")
            print(f">>> >>> Cannot find playlist {id} !!!")
        except Exception as ex:
            err_list.append(id)
            f.write(f">>> >>> {ex} : Error is occured at id {id} !!!\n")
            print(f">>> >>> {ex} : Error is occured at id {id} !!!")

    f.close()

    # save crwaling results
    saveInfoDict2Csv(pl_list=pl_list, songs_list=songs_list, setting=setting, start_idx=start_idx, end_idx=end_idx)
    print(f'err_index:{err_list}')


if __name__ == "__main__":
    main()
