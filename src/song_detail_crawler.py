from logging import Logger
from bs4 import BeautifulSoup
import requests
import textwrap

from src.song_detail.song_info_crawler import crawlSongInfo
from src.song_detail.song_daliy_chart_crawler import crawlSongDailyChart
from src.song_detail.song_lyrics_crawler import crawlSongLyrics
from src.song_detail.song_like_crawler import crawlSongLike


def crawlSongDetail(song_id: int, song_detail_url: str, log: Logger) -> dict:
    url = f"{song_detail_url}{song_id}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    log.info("- Crawling Song Detail : %d", song_id)
    info_data = crawlSongInfo(soup)
    log.info("info data : %s", str(info_data))
    listener_cnt, play_cnt = crawlSongDailyChart(soup)
    log.info("listener_cnt, play_cnt : %d, %d", listener_cnt, play_cnt)
    lyrics = crawlSongLyrics(soup)
    log.info("lyrics : %s", textwrap.shorten(lyrics, width=50, placeholder="...") if lyrics else lyrics)
    song_like = crawlSongLike(soup)
    log.info("Like : %d", song_like)

    info_data_upper_key = {key.upper(): item for key, item in info_data.items()}
    return {**info_data_upper_key, "SONG_ID": song_id, "LYRICS": lyrics, "LISTENER_CNT": listener_cnt, "PLAY_CNT": play_cnt, "SONG_LIKE": song_like}
