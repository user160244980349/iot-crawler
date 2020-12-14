from multiprocessing import Pool, cpu_count
from os.path import join

from html_sanitizer import Sanitizer

from config import sanitizer_settings, processed_policies, original_policies, policies_csv, resources
from crawler.tools import url_to_name
from tools.read.csv import csv_read


def clean_webpage(file: tuple):

    with open(file[0], "r", encoding="utf-8") as input_f:
        html = input_f.read()
        input_f.close()

        with open(file[1], "w", encoding="utf-8") as output_f:
            sanitizer = Sanitizer(sanitizer_settings)
            output_f.write(sanitizer.sanitize(html))
            output_f.close()


def clean(pipe_data: dict):
    threadpool = pipe_data["threadpool"]
    policies = csv_read(policies_csv)
    web_docs = [(join(resources, original_policies, url_to_name(p[0])),
                 join(resources, processed_policies, url_to_name(p[0]))) for p in policies]

    threadpool.map(clean_webpage, web_docs)

    return pipe_data
