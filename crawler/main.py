import logging
import sys
import traceback
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

from crawler.downloader import download
from crawler.pipeline import run_pipeline
from crawler.sanitizer import clean

from crawler.scraping.emarts.manufacturers import manufacturers
from crawler.scraping.policies import policies
from crawler.scraping.websites import websites


def main():

    pipe_data = dict()
    thread_count = int(cpu_count())
    print(f"Using thread count: {thread_count}")
    pipe_data["threadpool"] = ThreadPool(thread_count)

    try:

        pipeline = [
            manufacturers,
            websites,
            policies,
            download,
            clean,
        ]

        run_pipeline(pipeline, pipe_data)

    except Exception:
        ex_type, ex, tb = sys.exc_info()
        traceback.print_tb(tb)

    finally:
        print("Closing thread pool")
        p = pipe_data["threadpool"]
        p.close()
        p.join()
