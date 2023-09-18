import json
import logging
import os
from multiprocessing import Pool

import active_engines
from crawler.modules.module import Module


class Websites(Module):

    def __init__(self, products_json, websites_json):
        super(Websites, self).__init__()

        self.products_json = products_json
        self.websites_json = websites_json

    def run(self, p: Pool = None):
        self.logger.info("Searching websites")

        jobs = set([(r["manufacturer"], r["keyword"])
                    for r in self.records
                    if r["manufacturer"] is not None])
        webs = p.starmap(self.scrap_sites_urls, jobs)

        for item in self.records:
            for manufacturer, keyword, site in webs:
                if manufacturer == item["manufacturer"] \
                        and keyword == item["keyword"]:
                    item["website"] = site

    @classmethod
    def scrap_sites_urls(cls, manufacturer, keyword):
        logger = logging.getLogger(f"pid={os.getpid()}")
        logger.info(f"Searching: {manufacturer} {keyword}")

        for engine in active_engines.engines:
            try:
                site = engine.search(manufacturer, keyword)
                if site is not None:
                    logger.info(f"Got {site} website")
                    return manufacturer, keyword, site

            except Exception as e:
                logger.error(e)
                continue

        return manufacturer, keyword, None

    def bootstrap(self):
        with open(os.path.relpath(self.products_json), "r") as f:
            self.records = json.load(f)

    def finish(self):
        with open(os.path.relpath(self.websites_json), "w") as f:
            json.dump(self.records, f, indent=2)
