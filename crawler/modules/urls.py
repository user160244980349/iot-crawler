import logging
import os
from multiprocessing import Pool

import active_plugins
from crawler.modules.module import Module


class Urls(Module):

    def __init__(self):
        super(Urls, self).__init__()
        self.logger = logging.getLogger(f"pid={os.getpid()}")

    def bootstrap(self):
        pass

    def run(self, p: Pool = None):
        self.logger.info("Searching products")

        for plugin in active_plugins.plugins:
            plugin.scrap(p)

    def finish(self):
        pass
