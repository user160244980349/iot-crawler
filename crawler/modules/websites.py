import json
import logging
import os
from multiprocessing import Pool

import active_engines
import config
from crawler.modules.module import Module


class Websites(Module):

    def __init__(self):
        super(Websites, self).__init__(sync=False)
        self.logger = logging.getLogger(f"pid={os.getpid()}")

    def run(self, p: Pool = None):
        self.logger.info("Searching websites")

        if p is None:
            webs = [self.scrap_sites_urls(*i)
                    for i in set([(it['manufacturer'], it['keyword']) for it in self.records])]
        else:
            webs = p.starmap(self.scrap_sites_urls,
                             set([(it['manufacturer'], it['keyword']) for it in self.records]))

        for item in self.records:
            for manufacturer, keyword, site in webs:
                if manufacturer == item["manufacturer"] \
                        and keyword == item["keyword"]:
                    item["website"] = site

    @classmethod
    def scrap_sites_urls(cls, manufacturer, keyword):
        logger = logging.getLogger(f"pid={os.getpid()}")
        logger.info(f"Searching: {manufacturer} {keyword}")

        if manufacturer is None:
            return manufacturer, keyword, None

        logger = logging.getLogger(f"pid={os.getpid()}")

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
        with open(os.path.abspath(config.products_json), "r") as f:
            self.records = json.load(f)

    def finish(self):
        with open(os.path.abspath(config.websites_json), "w") as f:
            json.dump(self.records, f, indent=2)
