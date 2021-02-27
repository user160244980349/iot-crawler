import json
import logging
import os
from multiprocessing import Pool

import active_engines
import config
from crawler.modules.module import Module


class Websites(Module):

    def __init__(self):
        super(Websites, self).__init__()
        self.logger = logging.getLogger(f"pid={os.getpid()}")

    def run(self, p: Pool = None):
        self.logger.info("Searching websites")

        if p is None:
            webs = [self.scrap_sites_urls(i) for i in set([it["manufacturer"] for it in self.records])]
        else:
            webs = p.map(self.scrap_sites_urls, set([it["manufacturer"] for it in self.records]))

        for item in self.records:
            for manufacturer, site in webs:
                if manufacturer == item["manufacturer"]:
                    item["website"] = site

    @classmethod
    def scrap_sites_urls(cls, manufacturer):

        if manufacturer is None:
            return manufacturer, None

        logger = logging.getLogger(f"pid={os.getpid()}")

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

    def bootstrap(self):
        with open(os.path.abspath(config.products_json), "r") as f:
            self.records = json.load(f)

    def finish(self):

        with open(os.path.abspath(config.websites_json), "w") as f:
            json.dump(self.records, f, indent=2)
