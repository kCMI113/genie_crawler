from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date


def crawlReleaseDateInfo(id: int, driver: webdriver.Chrome) -> dict:
    album_detail_info = driver.find_element(By.CLASS_NAME, "album-detail-infos")
    info_zone = album_detail_info.find_element(By.CLASS_NAME, "info-zone")
    date_info = info_zone.find_elements(By.TAG_NAME, "li")[-1].text
    date_info = date_info.split(".")
    date_info = date(date_info[0], date_info[1], date_info[2])

    info = {"RELEASE_DATE": date_info}

    driver.close()

    return info
