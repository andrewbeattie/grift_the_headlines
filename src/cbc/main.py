"""
Download text from CBC riff the headline articles.
"""

from datetime import datetime
from api import get_cbc_urls
from src.cbc.article import CBCArticle
from helper import parse_date, parse_headline, parse_songs
from local import json_load, json_save

def create_data(data_list):
    all_data = []
    for data in data_list:
        values = {
            "url": None,
            "date": None,
            "songs": None,
            "headline": None
        }
        try:
            values.update(
                {"url": data["url"]}
                )
            article = CBCArticle(data["url"])
            text = article.text
            values.update(
                {"text": text}
                )
            values.update(
                {"date": data["date"].strftime("%Y-%m-%d")}
            )
            songs = parse_songs(text)
            values.update(
                {"songs": songs}
            )
            headline = parse_headline(text)
            values.update(
                {"headline": headline}
            )
            all_data.append(values)
        except:
            all_data.append(values)
    return all_data

class Runner:
    def __init__(self, date, search_str):
        self.date = date
        self.search_str = search_str

    def run(self):
        data_dict = get_cbc_urls(self.search_str, self.date)
        dataset = create_data(data_dict)
        fp = r".\data.json"
        json_save(fp, dataset)
