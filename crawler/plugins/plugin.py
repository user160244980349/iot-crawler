import json
import logging
import os
import re
from multiprocessing import Pool

from bs4 import BeautifulSoup

from crawler.product import Product
from crawler.web.driver import Driver
from tools.arrays import flatten_list


class Plugin:

    def __init__(self, keywords, pages, products_json,
                 cooldown=0., random_cooldown=0.):
        self.keywords = keywords
        self.pages = pages
        self.products_json = products_json
        self.to_query = re.compile(r"\s+")
        self.records = []
        self.cooldown = cooldown
        self.random_cooldown = random_cooldown

        self.logger = logging.getLogger(f"pid={os.getpid()}")

    def gen_search_urls(self, keyword, pages):
        raise NotImplementedError("Scraper is not implemented!")

    def scrap_products(self, url):
        raise NotImplementedError("Scraper is not implemented!")

    def get_product(self, url):
        raise NotImplementedError("Scraper is not implemented!")

    def scrap(self, p: Pool = None):
        try:
            with open(os.path.relpath(self.products_json), "r") as f:
                self.records = json.load(f)
        except FileNotFoundError:
            pass

        Product.counter = len(self.records)

        for keyword in self.keywords:
            search_urls = self.gen_search_urls(self.to_query.sub("+", keyword))

            items_urls = flatten_list(p.map(self.scrap_products, search_urls))
            found_items = p.map(self.get_product, items_urls)
            products = [Product(keyword=k, url=u, manufacturer=m)
                        for k, u, m in
                        [(keyword, *item) for item in found_items]]

            self.records.extend(products)

        with open(os.path.relpath(self.products_json), "w") as f:
            json.dump(self.records, f, indent=2)

    def scrap_page(self, url, templates):
        Driver().get(url, cooldown=self.cooldown,
                     random_cooldown=self.random_cooldown)
        markup = Driver().source()
        if markup:
            soup = BeautifulSoup(markup, "lxml").find("body")
            for t in templates:
                match = t(soup)
                if match is not None:
                    return match
