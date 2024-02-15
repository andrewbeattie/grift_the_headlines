"""
Download text from CBC riff the headline articles.
"""


import json
from datetime import datetime

from api import get_cbc_urls, get_text
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
            text = get_text(data["url"])
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

def run():
    search_str = "Day6 Riffed"
    date_filter = datetime(year=2023, month=1, day=1)
    data_dict = get_cbc_urls(search_str, date_filter)
    dataset = create_data(data_dict)
    fp = r".\data.json"
    json_save(fp, dataset)

if __name__ == "__main__":
    run()
