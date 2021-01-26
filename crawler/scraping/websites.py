import json
import logging
import os
import re
from multiprocessing import Pool

from bs4 import BeautifulSoup

from config import products_json, websites_json, resources
from crawler.web.driver import Driver


def scrap_sites(product):
    driver = Driver()
    markup = driver.get(f"https://www.google.com/search?q={product['manufacturer']}", delayed=True)
    soup = BeautifulSoup(markup, "html.parser").find("body").find("cite")

    product["website"] = None
    if soup is not None:
        if re.match(r"^.*\.(com|org|eu)$", soup.text) is not None:
            pattern = r"(^http://|^https://|www\.|/$)"
            product["website"] = f"https://{re.sub(pattern, '', soup.text)}"

    return product


def websites(p: Pool):
    logger = logging.getLogger(f"Main process")
    logger.info("Searching websites")

    with open(os.path.join(resources, products_json), "r") as f:
        products = json.load(f)

    web = p.map(scrap_sites, products)

    with open(os.path.join(resources, websites_json), "w") as f:
        json.dump(web, f)
