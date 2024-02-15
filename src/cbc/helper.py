"""
Helper functions used to process the text from CBC articles
"""

import regex as re
from typing import List
from datetime import datetime

def parse_songs(text):
    pattern = "(?<= clues were: )([^.]+)(?=.)"
    parser = re.compile(pattern)
    results = parser.findall(text)
    if results == []:
        pattern = "(?<= clues were )([^.]+)(?=.)"
        parser = re.compile(pattern)
        results = parser.findall(text)
        if results == []:
            pattern = "(?<= were: )([^.]+)(?=.)"
            parser = re.compile(pattern)
            results = parser.findall(text)
    if results == []:
        results = [None]
    return results[0]

def parse_headline(text):
    pattern = "(?<= the headline we were looking for: )([^.]+)(?=\\n\\n)"
    parser = re.compile(pattern)
    results = parser.findall(text)
    if results == []:
        pattern = "(?<= the headline we were looking for: )([^.]+)(?=.\\n)"
        parser = re.compile(pattern)
        results = parser.findall(text)
    if results == []:
        pattern = "(?<=for: )(.*)(?=\\n\\nCongratulations)"
        parser = re.compile(pattern)
        results = parser.findall(text)
    if results == []:
        results = [None]
    return results[0]

def parse_date(url) -> str:
    try:
        year = url.split("-")[-2]
        month = url.split("-")[-4]
        day = url.split("-")[-3]
        if len(year) == 2:
            pattern = "%y-%m-%d"
        elif len(year) == 4:
            pattern = "%Y-%m-%d"
        if int(month) > 12:
            if len(year) == 2:
                pattern = "%y-%d-%m"
            if len(year) == 4:
                pattern = "%Y-%d-%m"

        str_date = f"{year}-{month}-{day}"
        date = datetime.strptime(str_date, pattern)
        return date
    except:
        return None

def fix_url(url_str: str) -> str:
    return url_str.replace("//", "https://")
