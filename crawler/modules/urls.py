from multiprocessing import Pool

import active_plugins
from crawler.modules.module import Module


class Urls(Module):

    def __init__(self):
        super(Urls, self).__init__()

    def bootstrap(self):
        pass

    def run(self, p: Pool = None):
        self.logger.info("Searching urls")

        for plugin in active_plugins.plugins:
            plugin.scrap(p)

    def finish(self):
        pass
