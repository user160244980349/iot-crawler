import json
import os
import re
from multiprocessing import Pool

from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException

import config
from tools.arrays import flatten_list
from crawler.product import Product
from crawler.web.driver import Driver
from tools.exceptions import CaptchaException


class Plugin:

    def __init__(self, keywords, pages, sync=False):
        self.keywords = keywords
        self.pages = pages
        self.sync = sync
        self.to_query = re.compile(r"\s+")
        self.items = []

    def gen_search_urls(self, keyword, pages):
        raise NotImplementedError("Scraper is not implemented!")

    def scrap_products(self, url):
        raise NotImplementedError("Scraper is not implemented!")

    def get_product(self, url):
        raise NotImplementedError("Scraper is not implemented!")

    def on_captcha_exception(self):
        raise NotImplementedError("Scraper is not implemented!")

    def on_webdriver_exception(self):
        raise NotImplementedError("Scraper is not implemented!")

    def captcha(self, markup):
        return False

    def scrap(self, p: Pool = None):

        try:
            with open(os.path.abspath(config.products_json), "r") as f:
                self.items = json.load(f)
        except FileNotFoundError:
            pass

        for keyword in self.keywords:
            search_urls = self.gen_search_urls(self.to_query.sub("+", keyword), self.pages)

            items_urls = flatten_list([self.scrap_products(url) for url in search_urls] \
                         if p is None or self.sync else p.map(self.scrap_products, search_urls))

            found_items = [self.get_product(product) for product in items_urls] \
                          if p is None or self.sync else p.map(self.get_product, items_urls)

            products = [Product(keyword=d[0], url=d[1], manufacturer=d[2])
                        for d in [(keyword, *item) for item in found_items]]

            self.items.extend(products)

        with open(os.path.abspath(config.products_json), "w") as f:
            json.dump(self.items, f, indent=2)

    def scrap_page(self, url, templates):

        driver = Driver()
        net_error = 0

        markup = ""
        while True:

            try:
                markup = driver.get(url)

                if self.captcha(markup):
                    raise CaptchaException()

                break

            except WebDriverException:
                self.on_webdriver_exception()
                net_error += 1
                if net_error > config.max_error_attempts:
                    break

            except CaptchaException:
                self.on_captcha_exception()
                net_error += 1
                if net_error > config.max_captcha_attempts:
                    break

        soup = BeautifulSoup(markup, "lxml").find("body")
        for t in templates:
            match = t(soup)
            if match is not None:
                return match
