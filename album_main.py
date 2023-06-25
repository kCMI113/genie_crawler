import os
import re
import hydra
import pandas as pd
from tqdm import tqdm
from omegaconf import DictConfig

from selenium import webdriver
from selenium.webdriver.common.by import By

from src.utils import resizeImg


@hydra.main(version_base="1.2", config_path="configs", config_name="config.yaml")
def main(config: DictConfig = None) -> None:
    file_path = config.out_dir
    playlist_file = "playlists.csv"
    song_file = "songs.csv"

    pl_df = pd.read_csv(os.path.join(file_path, playlist_file))
    song_df = pd.read_csv(os.path.join(file_path, song_file))

    non_album_ids = list(song_df[song_df["IMG_PATH"].apply(lambda x: not bool(re.search(".png|.JPG|.PNG|.jpg", x)))]["ALBUM_ID"])
    album_url = "https://www.genie.co.kr/detail/albumInfo?axnm="

    album_img_list = []
    for id in tqdm(non_album_ids):
        link = album_url + str(id)

        op = webdriver.ChromeOptions()
        op.add_argument("--headless")

        driver = webdriver.Chrome(options=op)
        driver.get(url=link)

        details = driver.find_element(By.CLASS_NAME, "album-detail-infos")
        photo = details.find_element(By.CLASS_NAME, "photo-zone")
        img_path = (photo.find_element(By.TAG_NAME, "a")).get_attribute("href")
        resized_img_path = resizeImg(img_path[: img_path.find("/dims")], config.img_resize, config.max_resize)

        info = {
            "ALBUM_ID": id,
            "IMG_PATH": resized_img_path,
        }
        print(f"ALBUM_ID: {id} / IMG_PATH {resized_img_path} ... ")

        album_img_list.append(info)
        driver.close()

    album_img_df = pd.DataFrame(album_img_list)

    new_album_img_path = os.path.join(file_path, "new_album_imgs.csv")
    album_img_df.to_csv(new_album_img_path, index=False)


if __name__ == "__main__":
    main()
