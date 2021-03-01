import logging
import os
import re
from multiprocessing import Pool

from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException

import config
from crawler.product import Product
from crawler.web.driver import Driver
from tools.arrays import flatten_list


class Plugin:

    def __init__(self, keywords, pages, sync=False):
        self.keywords = keywords
        self.pages = pages
        self.sync = sync

    def gen_search_urls(self, keyword, pages):
        raise NotImplementedError("Scraper is not implemented!")

    def scrap_products(self, url):
        raise NotImplementedError("Scraper is not implemented!")

    def get_product(self, product):
        raise NotImplementedError("Scraper is not implemented!")

    def scrap(self, p: Pool = None):

        items = []

        for keyword in self.keywords:
            keyword_escaped = re.sub(r"\s", "+", keyword)
            search_urls = self.gen_search_urls(keyword_escaped, self.pages)

            if p is None or self.sync:
                items_urls = [self.scrap_products(url) for url in search_urls]
            else:
                items_urls = p.map(self.scrap_products, search_urls)

            items_urls = flatten_list(items_urls)

            products = [Product(url=url) for url in items_urls]

            if p is None:
                found_items = [self.get_product(product) for product in products]
            else:
                found_items = p.map(self.get_product, products)

            for found_item in found_items:
                found_item["keyword"] = keyword

            items.extend(found_items)

        return items

    @classmethod
    def scrap_products_base(cls, url, template, captcha=lambda m: False):

        logger = logging.getLogger(f"pid={os.getpid()}")
        logger.info(f"Scrapping page: {url}")

        driver = Driver()
        net_error = 0

        while True:
            try:
                markup = driver.get(url)

                if captcha(markup):
                    return []

                soup = BeautifulSoup(markup, "lxml").find("body")
                return template(soup)

            except WebDriverException:
                logger.warning(f"Web driver exception, potentially net error")
                driver.change_proxy()
                net_error += 1
                if net_error > config.max_error_attempts:
                    return []

    @classmethod
    def get_product_base(cls, product, templates, captcha=lambda m: False):
        logger = logging.getLogger(f"pid={os.getpid()}")

        driver = Driver()
        net_error = 0

        while True:
            try:
                markup = driver.get(product["url"])

                if captcha(markup):
                    return product

                soup = BeautifulSoup(markup, "lxml").find("body")

                for t in templates:
                    product["manufacturer"] = t(soup)
                    if product["manufacturer"] is not None:
                        break

                return product

            except WebDriverException:
                logger.warning(f"Web driver exception, potentially net error")
                driver.change_proxy()
                net_error += 1
                if net_error > config.max_error_attempts:
                    return product
