import logging
import os
import re
from multiprocessing import Pool
from time import sleep

from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException

import config
from crawler.product import Product
from crawler.web.driver import Driver
from tools.arrays import flatten_list
from tools.exceptions import CaptchaException


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

            if p is None or self.sync:
                found_items = [self.get_product(product) for product in products]
            else:
                found_items = p.map(self.get_product, products)

            for found_item in found_items:
                found_item["keyword"] = keyword

            items.extend(found_items)

        return items

    def captcha(self, markup):
        return False

    def scrap_products_base(self, url, template):

        logger = logging.getLogger(f"pid={os.getpid()}")
        logger.info(f"Scrapping page: {url}")

        driver = Driver()
        net_error = 0

        while True:
            try:
                markup = driver.get(url)

                if self.captcha(markup):
                    raise CaptchaException()

                soup = BeautifulSoup(markup, "lxml").find("body")
                return template(soup)

            except WebDriverException:
                logger.warning(f"Web driver exception, potentially net error")
                sleep(config.retry_period)

                driver.change_proxy()
                driver.change_useragent()
                driver.restart_session()

                net_error += 1
                if net_error > config.max_error_attempts:
                    return []

            except CaptchaException:
                logger.error("Sorry, we just need to make sure you're not a robot.")
                sleep(config.retry_period)

                driver.change_proxy()
                driver.change_useragent()
                driver.restart_session()

                net_error += 1
                if net_error > config.max_captcha_attempts:
                    return []

    def get_product_base(self, product, templates):
        logger = logging.getLogger(f"pid={os.getpid()}")

        driver = Driver()
        net_error = 0

        while True:

            try:

                markup = driver.get(product["url"])

                if self.captcha(markup):
                    raise CaptchaException()

                soup = BeautifulSoup(markup, "lxml").find("body")

                for t in templates:
                    product["manufacturer"] = t(soup)
                    if product["manufacturer"] is not None:
                        logger.info(f"Got manufacturer {product['manufacturer']}")
                        break

                return product

            except WebDriverException:
                logger.warning(f"Web driver exception, potentially net error")
                sleep(config.retry_period)

                driver.change_proxy()
                driver.change_useragent()
                driver.restart_session()

                net_error += 1
                if net_error > config.max_error_attempts:
                    return product

            except CaptchaException:
                logger.error("Sorry, we just need to make sure you're not a robot.")
                sleep(config.retry_period)

                driver.change_proxy()
                driver.change_useragent()
                driver.restart_session()

                net_error += 1
                if net_error > config.max_captcha_attempts:
                    return product
