from tools.read.csv import csv_write


class Plugin:

    def __init__(self, threadpool, keywords, pages):
        self.threadpool = threadpool
        self.keywords = keywords
        self.pages = pages

    def gen_urls(self, keyword):
        raise NotImplementedError("Scrap is not implemented!")

    def scrap(self):
        raise NotImplementedError("Scrap is not implemented!")
