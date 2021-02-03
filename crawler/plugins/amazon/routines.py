import logging
import os
import re
from time import sleep

from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException

import config
from crawler.plugins.amazon.templates import template1, template2, template3, product_template
from crawler.web.driver import Driver


templates = [
    template1,
    template2,
    template3
]


def get_product(url):

    logger = logging.getLogger(f"pid={os.getpid()} | Amazon")

    product = dict()
    product["url"] = url
    product["manufacturer"] = None

    if url is None:
        return product

    sleep(3)
    driver = Driver()
    markup = driver.get(url)

    if re.search("Sorry, we just need to make sure you're not a robot.", markup):
        logger.error("Sorry, we just need to make sure you're not a robot.")
        return product

    soup = BeautifulSoup(markup, "lxml").find("body")

    for t in templates:
        product["manufacturer"] = t(soup)
        if product["manufacturer"] is not None:
            break

    return product


def scrap_products(url):

    if url is None:
        return []

    logger = logging.getLogger(f"pid={os.getpid()} | Amazon")
    logger.info(f"Scrapping page: {url}")

    sleep(3)
    driver = Driver()
    markup = driver.get(url)

    net_error = 0
    while True:
        logger.warning(f"Getting to {url}")
        try:
            soup = BeautifulSoup(markup, "lxml").find("body")
            return product_template(soup)

        except WebDriverException as e:
            logger.warning(f"Web driver exception, potentially net error")
            driver.change_proxy()
            net_error += 1
            if net_error > config.max_error_attempts:
                return []
