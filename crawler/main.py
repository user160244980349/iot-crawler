from crawler.sanitizer.sanitizer import clean
from crawler.downloader.downloader import download
from crawler.name_resolver.resolver import resolve
from crawler.pipeline import run_pipeline


def main():

    pipeline = [
        resolve,
        download,
        clean
    ]

    pipeline_data = dict()
    run_pipeline(pipeline, pipeline_data)
