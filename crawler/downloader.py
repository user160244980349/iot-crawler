from multiprocessing import Pool, cpu_count
from os.path import join

from config import policies_csv, original_policies, resources
from crawler.exceptions import UrlNotFound
from crawler.tools import url_to_name
from crawler.web.driver_factory import DriverFactory
from tools.read.csv import csv_read


def store(file: tuple):
    driver = DriverFactory.get()
    markup = driver.get(file[0])

    try:
        with open(file[1], "w", encoding="utf-8") as f:
            f.write(markup)
            f.close()
    except UrlNotFound as e:
        print(e)


def download(pipe_data: dict):
    threadpool = pipe_data["threadpool"]
    policies = csv_read(policies_csv)
    web_docs = [(p[0], join(resources, original_policies, url_to_name(p[0]))) for p in policies]
    threadpool.map(store, web_docs)
    return pipe_data
