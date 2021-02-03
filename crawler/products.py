import json
import logging
import os
from multiprocessing import Pool

from active_plugins import plugins
from config import products_json, resources


def products(p: Pool):
    logger = logging.getLogger(f"pid={os.getpid()}")
    logger.info("Searching products")

    items = []

    for plugin in plugins:
        items.extend(plugin.scrap(p))

    for i in range(len(items)):
        items[i]["id"] = i

    with open(os.path.join(resources, products_json), "w") as f:
        json.dump(items, f)
