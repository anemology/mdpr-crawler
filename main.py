import argparse
import os
import shutil
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, url: str):
        self._base_url = base_url(url)
        self.new_urls = []
        self.photo_urls = []  # photo page

    def crawl(self):
        pass

    def _get_news_urls(self):
        pass

    def _get_photo_urls(self):
        pass

    def _get_img_urls(self):
        # deal with first image
        # .c-image__inner pg-photo__image img
        pass


def main(url: str):
    if "news/detail" in url:
        pass
    elif "photo/detail" in url:
        pass
    else:
        url = url.replace("news", "news/detail")

    base = base_url(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    photo_page = soup.select_one(".pg-articleDetail__showAllPhoto > a")
    if not photo_page:
        return

    response = requests.get(urljoin(base, photo_page["href"]))
    soup = BeautifulSoup(response.text, "html.parser")
    img_item = soup.select(".pg-photo__webImageList > .pg-photo__webImageListItem img")

    img_urls = [file_url(x["src"]) for x in img_item]

    for index, url in enumerate(img_urls, start=1):
        r = requests.get(url, stream=True)
        with open(f"{index:02d}_{os.path.basename(url)}", "wb") as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


def base_url(url: str):
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}"


def file_url(url: str):
    p = urlparse(url)
    return p._replace(query="", fragment="").geturl()


if __name__ == "__main__":
    # TODO: argparse
    url = "https://mdpr.jp/news/2908083"
    # https://mdpr.jp/photo/detail/10669294

    main(url)
