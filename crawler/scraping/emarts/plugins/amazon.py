import re
from random import random
from time import sleep

from bs4 import BeautifulSoup

from config import cooldown, multiplier
from crawler.scraping.emarts.plugins.plugin import Plugin
from crawler.web.driver_factory import DriverFactory


def manufacturer(url):
    sleep(cooldown + random() * multiplier)
    driver = DriverFactory.get()
    markup = driver.get(url)

    body = BeautifulSoup(markup, "html.parser").find("body")

    div = body.find("div", {"id": "detailBullets_feature_div"})
    if div is not None:
        for li in div.ul.findChildren("li"):
            spans = li.span.findChildren("span")
            text = re.sub(r"[\n\s]", "", spans[0].text)
            if re.match("^Manufacturer:$", text):
                return re.sub(r"[\"\',\n]", "", spans[1].text).lower()

    div = body.find("table", {"id": "productDetails_detailBullets_sections1"})
    if div is not None:
        for tr in div.tbody.findChildren("tr"):
            text = re.sub(r"[\n\s]", "", tr.th.text)
            if re.search("^Manufacturer$", text):
                return re.sub(r"[\"\',\n]", "", tr.td.text).lower()

    div = body.find("table", {"id": "productDetails_techSpec_section_1"})
    if div is not None:
        for tr in div.tbody.findChildren("tr"):
            text = re.sub(r"[\n\s]", "", tr.th.text)
            if re.search("^Manufacturer$", text):
                return re.sub(r"[\"\',\n]", "", tr.td.text).lower()

    if re.search("Sorry, we just need to make sure you're not a robot.", markup):
        print("Sorry, we just need to make sure you're not a robot.")

    print(url)


def scrap_products(url):
    sleep(cooldown + random() * multiplier)
    driver = DriverFactory.get()
    markup = driver.get(url)
    soup = BeautifulSoup(markup, "html.parser").find("body")
    return [f"https://www.amazon.com{items.findChild('a').get('href')}"
            for items in soup.findAll("div", {"data-component-type": "s-search-result"})]


class Amazon(Plugin):

    def __init__(self, tp, keywords, pages):
        super().__init__(tp, keywords, pages)

    def gen_urls(self, keyword):
        return [f"https://www.amazon.com/s?k={keyword}&page={p}&s=review-rank"
                for p in range(1, self.pages + 1)]

    def scrap(self):
        manufacturers = []
        for keyword in self.keywords:
            keyword_escaped = re.sub(r"\s", "+", keyword)
            urls = self.gen_urls(keyword_escaped)
            urls = self.threadpool.map(scrap_products, urls)
            urls = [item for sub_urls in urls for item in sub_urls]
            result = self.threadpool.map(manufacturer, urls)
            manufacturers.extend([item for item in result
                                  if item is not None])

        manufacturers = [[item] for item in set(manufacturers)]

        return manufacturers
