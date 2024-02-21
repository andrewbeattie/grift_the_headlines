"""
Interactions with CBC API and CBC website.
"""

import ast
import requests
from typing import Optional
from datetime import datetime
from src.cbc.article import CBCArticle
from helper import fix_url
from dateutil.parser import parse

def get_date(url):
    """
    Look to implement a more reasonable way to filter by date.
    """
    article = CBCArticle(url)
    return article.publish_date

def get_text(url):
    """
    Given a text based article URL return the article text
    """
    try:
        article = CBCArticle(url)

        return article.text
    except:
        return ""

def get_cbc_urls(search_str: str, date: Optional[datetime] = None):
    """
    For a given keyword search for all urls.

    In addition filters the content with the following parameters.
        section: radio
        media: all
    
    It is ordered by date descending and returns a maximum of 10 entries per a page.
    """
    all_url = []
    search_flag = True
    n = 1

    while search_flag == True:
        params = {
            "q": search_str,
            "section": "radio",
            "sortOrder": "date",
            "media": "all",
            "page": n
        }

        res = requests.get(
            "https://www.cbc.ca/search_api/v1/search",
            params=params
            )

        if res.status_code == 200:
            res_list = ast.literal_eval(res.text)
            
            from helper import parse_date

            for r in res_list:
                if date != None:
                    r["date"] = parse_date(r["url"])
                    if r["date"] == None:
                        url = fix_url(r["url"])
                        r["date"] = get_date(url)
                    if r["date"] < date:
                        search_flag = False
                        break
                    r["url"] = fix_url(r["url"])
                all_url.append(r)
            n += 1
        else:
            search_flag = False

    return all_url


if __name__ == "__main__":
    valid_url_data = get_cbc_urls(
        search_str="Riffed",
        date=datetime(year=2023, month=12, day=30)
    )
