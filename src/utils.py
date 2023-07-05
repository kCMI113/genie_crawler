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


def saveInfoDict2Csv(pl_list: list[dict], songs_list: list[dict], setting: DictConfig, start_idx: int, end_idx: int) -> None:
    createDirectory(setting.out_dir)
    search_range = str(start_idx) + "_" + str(end_idx) + "_"

    pl_path = os.path.join(setting.out_dir, search_range + setting.pl_filename)
    song_path = os.path.join(setting.out_dir, search_range + setting.song_filename)

    # save playlist csv
    pl_df = pd.DataFrame(pl_list)
    pl_df.to_csv(pl_path, index=False)

    # save songs csv
    songs_df = pd.DataFrame(songs_list)
    songs_df.to_csv(song_path, index=False)


def saveDict2Csv(data: list[dict], save_path: str):
    df = pd.DataFrame(data)
    df.to_csv(save_path, index=False)


def resizeImg(path: str, size: int, max_size: int) -> str:
    if size > max_size:
        raise Exception(f"[ERROR] img_resize ({size}) must be smaller than max_size ({max_size})")
    else:
        return path + "/dims/resize/Q_" + str(size) + "," + str(size)


def getLastPlaylistId(link: str) -> int:
    op = webdriver.ChromeOptions()
    op.add_argument("--headless")

    driver = webdriver.Chrome(options=op)
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


def tranlateSongInfoAttrToEng(attr: str) -> str:
    ATTR_URL_TO_ENG = {
        "https://image.genie.co.kr/imageg/web/detail/txt_1.png": "info_artist_type",
        "https://image.genie.co.kr/imageg/web/detail/txt_2.png": "info_artist_active_years",
        "https://image.genie.co.kr/imageg/web/detail/txt_3.png": "info_artist_debut",
        "https://image.genie.co.kr/imageg/web/detail/txt_4.png": "info_artist_nationality",
        "https://image.genie.co.kr/imageg/web/detail/txt_5.png": "info_artist_name",
        "https://image.genie.co.kr/imageg/web/detail/txt_6.png": "info_album_title",
        "https://image.genie.co.kr/imageg/web/detail/txt_7.png": "info_genre",
        "https://image.genie.co.kr/imageg/web/detail/txt_8.png": "info_play_time",
        "https://image.genie.co.kr/imageg/web/detail/txt_9.png": "info_image_video",
        "https://image.genie.co.kr/imageg/web/detail/txt_10.png": "info_genre_style",
        "https://image.genie.co.kr/imageg/web/detail/txt_11.png": "info_publisher",
        "https://image.genie.co.kr/imageg/web/detail/txt_12.png": "info_publish_date",
        "https://image.genie.co.kr/imageg/web/detail/txt_13.png": "info_agency",
        "https://image.genie.co.kr/imageg/web/detail/txt_18.png": "info_composer",
        "https://image.genie.co.kr/imageg/web/detail/txt_19.png": "info_composer",
        "https://image.genie.co.kr/imageg/web/detail/txt_20.png": "info_lyricst",
        "https://image.genie.co.kr/imageg/web/detail/txt_21.png": "info_arranger",
    }

    return ATTR_URL_TO_ENG[attr]
