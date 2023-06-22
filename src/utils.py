import os
import pandas as pd
from datetime import datetime
from omegaconf import DictConfig

from selenium import webdriver
from selenium.webdriver.common.by import By


def createDirectory(dir: str) -> None:
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
            print(f">>> {dir} is created !!!")
    except OSError:
        print(f"[ERROR] Creating {path} is failed !!!")


def setLogFile(setting: DictConfig) -> str:
    # get Timestamp
    now = datetime.now()
    now = now.strftime("%m%d_%H%M")

    # create log dir
    createDirectory(setting.log_dir)

    # set path
    file_name = now + "_logs.txt"
    log_path = os.path.join(setting.log_dir, file_name)
    return log_path


def saveInfoDict2Csv(pl_list: list[dict], songs_list: list[dict], setting: DictConfig) -> None:
    createDirectory(setting.out_dir)

    pl_path = os.path.join(setting.out_dir, setting.pl_filename)
    song_path = os.path.join(setting.out_dir, setting.song_filename)

    # save playlist csv
    pl_df = pd.DataFrame(pl_list)
    pl_df.to_csv(pl_path, index=False)

    # save songs csv
    songs_df = pd.DataFrame(songs_list)
    songs_df.to_csv(song_path, index=False)


def resizeImg(path: str, size: int, max_size: int) -> str:
    if size > max_size:
        raise Exception(f"[ERROR] img_resize ({size}) must be smaller than max_size ({max_size})")
    else:
        return path + "/dims/resize/Q_" + str(size) + "," + str(size)


def getLastPlaylistId(link: str) -> int:
    driver = webdriver.Chrome()
    driver.get(url=link)

    items = driver.find_elements(By.CLASS_NAME, "item_cover")

    ids = []
    for item in items:
        click_link = (item.find_element(By.CLASS_NAME, "cover")).get_attribute("onclick")

        start_idx = click_link.find("('")
        end_idx = click_link.find("')")
        id = int(click_link[start_idx + 2 : end_idx])
        ids.append(id)

    driver.close()

    return max(ids)
