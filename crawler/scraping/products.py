import json
import logging
import os
from multiprocessing import Pool

from config import products_json, resources
from plugins.active_plugins import scrap_plugins


def scrap_products(p: Pool):
    logger = logging.getLogger(f"Main process")
    logger.info("Searching products")

    products = []

    for plugin in scrap_plugins:
        products.extend(plugin.scrap(p))

    with open(os.path.join(resources, products_json), "w") as f:
        json.dump(products, f)
