import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

def set_logfile() -> str:
    now = datetime.now()
    now = now.strftime('%m%d_%H%M')
    file_name = now + "_logs.txt"

    return file_name


def resize_img(path: str, size:int = 140) -> str:
    return path + "/dims/resize/Q_" + str(size) + "," + str(size)

def get_last_playlist_id(link: str) -> int:
    driver = webdriver.Chrome()
    driver.get(url=link)
    
    items = driver.find_elements(By.CLASS_NAME, "item_cover")
    
    ids = []
    for item in items:
        click_link = (item.find_element(By.CLASS_NAME, "cover")).get_attribute("onclick")
        
        start_idx = click_link.find("('")
        end_idx = click_link.find("')")
        id = int(click_link[start_idx + 2:end_idx])
        ids.append(id)
    
    driver.close()
    
    return max(ids)



