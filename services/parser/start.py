import os
import re
import requests

from itertools import chain
from bs4 import BeautifulSoup
from datetime import datetime
from collections import namedtuple
from time import sleep
from typing import List

from lib.db import Pool
from lib.log import log
from lib.config import Config


Article = namedtuple(
    'Article',
    ["title", "image_url", "published_date", "parsed_date"]
)
Result = List[Article]

url = 'http://mosday.ru/news/tags.php?metro'
body_xpath = '//center/table/tbody'
date_regex = re.compile(r"^([0-9\.]{10}).(\d{0,2}:?\d{0,2})")


def get_result(url: str) -> Result:
    res = requests.get(url=url)
    result = []
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        tables = soup.find_all(
            "table",
            attrs={"width": "95%", "cellspacing": "10"}
        )
        articles = list(chain(*[t.find_all('tr') for t in tables]))
        for article in articles:
            image_tag, title_tag = article.find_all('td')
            if image := image_tag.find('img'):
                image = f"http://mosday.ru/news/{image.attrs['src']}"
            title_ref = title_tag.find('a')
            if title_ref.attrs.get('title') != 'перейти на стедующую страницу':
                title = title_ref.text
                match = date_regex.search(title_tag.text)
                if match:
                    date = match.group(1)
                    time = match.group(2) or "00:00"
                    published_date = datetime.strptime(
                        f"{date} {time}",
                        "%d.%m.%Y %H:%M"
                    )
                else:
                    published_date = datetime.now()
                parsed_date = datetime.now()
                result.append(
                    Article(title, image, published_date, parsed_date)
                )
    log.info("Got %d articles!", len(result))
    return result


def save_result(result: Result):
    query = """
        INSERT INTO article (
            title,
            image_url,
            published_date,
            parsed_date
        )
        VALUES (
            %(title)s,
            %(image_url)s,
            %(published_date)s,
            %(parsed_date)s
        )
        ON CONFLICT (title, published_date)
        DO NOTHING
    """
    with Pool.get_db() as db:
        cursor = db.cursor()
        for article in result:
            cursor.execute(query, article._asdict())
        db.commit()
        log.info("Saving news completed!")


if __name__ == "__main__":
    Config.setup("parser")
    log.info("Start collect news")
    time_delay = int(os.environ.get("PARSE_DELAY"))
    while True:
        try:
            result = get_result(url=url)
            save_result(result)
        except KeyboardInterrupt:
            log.info("Interrupted by user")
            raise
        except Exception:
            log.exception("Failed to collect news!")
        finally:
            sleep(time_delay)
