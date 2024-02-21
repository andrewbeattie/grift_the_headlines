import re
from datetime import datetime
from newspaper import Article

class CBCArticle(Article):
    """
    Article parser backed upon newspaper package with modified method for parsing the date published specific for CBC articles.
    """
    def __init__(self, url: str, language: str = 'en'):
        super().__init__(url, language=language)
        self.download()
        self.parse()
        self.get_publish_date()

    def get_publish_date(self) -> str:
        """
        extract pattern from "datePublished":"2024-02-09T05:00Z"
        Example:
            "datePublished":"2024-02-09T05:00Z"
        """
        pattern = r"datePublished\":\"(.*?)\""
        match = re.search(pattern, self.html)
        if match:
            date = match.group(1)
            self.publish_date = datetime.strptime(date, "%Y-%m-%dT%H:%MZ")
