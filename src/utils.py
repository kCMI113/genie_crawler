import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime


def createDirectory(dir: str):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
            print(f">>> {dir} is created !!!")
    except OSError:
        print(f"[ERROR] Creating {path} is failed !!!")


def setLogFile() -> str:
    # get Timestamp
    now = datetime.now()
    now = now.strftime("%m%d_%H%M")

    # set path
    file_name = now + "_logs.txt"
    out_dir = "logs/"
    createDirectory(out_dir)
    file_path = os.path.join(out_dir, file_name)

    return file_path


def saveSongs2Csv(songs_list: list[dict]) -> None:
    # set path
    file_name = "song_info.csv"
    out_dir = "outputs/"
    createDirectory(out_dir)
    file_path = os.path.join(out_dir, file_name)

    # save csv
    songs_df = pd.DataFrame(songs_list)
    songs_df.to_csv(file_path, index=False)


def resizeImg(path: str, size: int = 140) -> str:
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
