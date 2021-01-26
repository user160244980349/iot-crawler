from multiprocessing import Pool


class Plugin:

    def __init__(self, keywords, pages):
        self.keywords = keywords
        self.pages = pages

    def gen_search_urls(self, keyword):
        raise NotImplementedError("Scrap is not implemented!")

    def scrap(self, p: Pool):
        raise NotImplementedError("Scrap is not implemented!")
