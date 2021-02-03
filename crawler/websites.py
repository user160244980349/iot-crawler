import json
import logging
import os
from multiprocessing import Pool
from os import getpid

import active_engines
import config
from crawler.web.driver import Driver


def websites(p: Pool = None):
    logger = logging.getLogger(f"pid={getpid()}")
    logger.info("Searching websites")

    with open(os.path.join(config.resources, config.products_json), "r") as f:
        items = json.load(f)

    if p is None:
        webs = [scrap_sites_urls(item)
                for item in set([it["manufacturer"] for it in items])]
        Driver.close()
    else:
        webs = p.map(scrap_sites_urls, set([it["manufacturer"] for it in items]))

    for item in items:
        for manufacturer, site in webs:
            if manufacturer == item["manufacturer"]:
                item["website"] = site

    with open(os.path.join(config.resources, config.websites_json), "w") as f:
        json.dump(items, f)


def scrap_sites_urls(manufacturer):
    if manufacturer is None:
        return manufacturer, None

    logger = logging.getLogger(f"pid={getpid()}")

    for engine in active_engines.engines:
        try:
            site = engine.search(manufacturer)
            if site is not None:
                logger.info(f"Got {site} website")
                return manufacturer, site
        except Exception as e:
            logger.error(e)
            continue

    return manufacturer, None
