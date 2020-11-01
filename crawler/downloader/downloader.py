from multiprocessing import Pool, cpu_count
from os.path import join
from pprint import pprint
from urllib.request import urlopen

from config import original_policies, urls
from crawler.downloader.exceptions import UrlNotFound


def store(file: tuple):
    content = urlopen(file[0])

    try:
        with open(file[1], "wb") as f:
            f.write(content.read())
            f.close()
    except UrlNotFound as e:
        print(e)


def download(pipe_data: dict):

    web_docs = list(zip(pipe_data["urls"], pipe_data["raw_markup"]))

    with Pool(cpu_count()) as pool:
        pool.map(store, web_docs)
        pool.close()
        pool.join()

    return pipe_data
