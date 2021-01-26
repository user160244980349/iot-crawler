import logging
import re
from multiprocessing import Pool
from os import getpid

from bs4 import BeautifulSoup

from crawler.web.driver import Driver
from plugins.plugin import Plugin


def template1(body):
    div = body.find("div", {"id": "detailBullets_feature_div"})
    if div is not None:
        for li in div.ul.findChildren("li"):
            spans = li.span.findChildren("span")
            text = re.sub(r"[\n\s]", "", spans[0].text)
            if re.match("^Manufacturer:$", text):
                return re.sub(r"[\"\',\n]", "", spans[1].text).lower()
    return None


def template2(body):
    div = body.find("table", {"id": "productDetails_detailBullets_sections1"})
    if div is not None:
        for tr in div.tbody.findChildren("tr"):
            text = re.sub(r"[\n\s]", "", tr.th.text)
            if re.search("^Manufacturer$", text):
                return re.sub(r"[\"\',\n]", "", tr.td.text).lower()
    return None


def template3(body):
    div = body.find("table", {"id": "productDetails_techSpec_section_1"})
    if div is not None:
        for tr in div.tbody.findChildren("tr"):
            text = re.sub(r"[\n\s]", "", tr.th.text)
            if re.search("^Manufacturer$", text):
                return re.sub(r"[\"\',\n]", "", tr.td.text).lower()
    return None


def get_product(url):
    logger = logging.getLogger(f"pid={getpid()}")

    driver = Driver()
    markup = driver.get(url, delayed=True)

    body = BeautifulSoup(markup, "html.parser").find("body")

    product = dict()
    product["url"] = url
    product["manufacturer"] = None

    # Errors below
    if re.search("Sorry, we just need to make sure you're not a robot.", markup):
        logger.error("Sorry, we just need to make sure you're not a robot.")
        return product

    if product["manufacturer"] is None:
        product["manufacturer"] = template1(body)

    if product["manufacturer"] is None:
        product["manufacturer"] = template2(body)

    if product["manufacturer"] is None:
        product["manufacturer"] = template3(body)

    if product["manufacturer"] is None:
        logger.error(f"This product has no manufacturer: {url}")

    return product


def scrap_products(url):
    logger = logging.getLogger(f"pid={getpid()}")
    logger.info(f"Scrapping page: {url}")

    driver = Driver()
    markup = driver.get(url, delayed=True)
    soup = BeautifulSoup(markup, "html.parser").find("body")

    return [f"https://www.amazon.com{items.findChild('a').get('href')}"
            for items in soup.findAll("div", {"data-component-type": "s-search-result"})]


def flatten_list(list_of_lists):
    return [item for sub_list in list_of_lists for item in sub_list]


class Amazon(Plugin):

    def __init__(self, keywords, pages):
        super().__init__(keywords, pages)

    def gen_search_urls(self, keyword):
        return [f"https://www.amazon.com/s?k={keyword}&page={p}&s=review-rank"
                for p in range(1, self.pages + 1)]

    def scrap(self, p: Pool):

        products = []

        for keyword in self.keywords:
            keyword_escaped = re.sub(r"\s", "+", keyword)
            search_urls = self.gen_search_urls(keyword_escaped)
            products_urls = p.map(scrap_products, search_urls)
            products_urls = flatten_list(products_urls)
            results = p.map(get_product, products_urls)

            for result in results:
                result["keyword"] = keyword

            products.extend(results)

        for i in range(len(products)):
            products[i]["id"] = i

        return products
