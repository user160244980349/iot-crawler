from config import manufacturers_csv
from crawler.scraping.emarts.plugins.amazon import Amazon
from tools.read.csv import csv_write


def manufacturers(pipe_data: dict):

    threadpool = pipe_data["threadpool"]

    plugins = [
        Amazon(threadpool, ["smart scales", "smart watches", "smart locks", "smart bulbs"], 10),
        # Amazon(threadpool, ["smart scales"], 1),
    ]

    ms = []
    for p in plugins:
        ms.extend(p.scrap())

    csv_write(ms, manufacturers_csv)

    return pipe_data
