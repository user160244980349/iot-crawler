import json
import logging
import os
from multiprocessing import Pool
from os.path import join

from config import original_policies, resources, policies_json, downloaded_json
from crawler.web.driver import Driver
from tools.text import url_to_name


def store(item):
    driver = Driver()
    markup = driver.get(item["policy"])

    item["policy_hash"] = None
    item["original_policy"] = None

    if markup is None:
        return item

    item["policy_hash"] = hash(markup)
    item["original_policy"] = join(resources, original_policies, url_to_name(item["policy"]))

    with open(item["original_policy"], "w", encoding="utf-8") as f:
        f.write(markup)
        f.close()

    return item


def download(p: Pool):
    logger = logging.getLogger(f"Main process")
    logger.info("Download")

    with open(os.path.join(resources, policies_json), "r") as f:
        items = json.load(f)

    downloaded = p.map(store, items)

    with open(os.path.join(resources, downloaded_json), "w") as f:
        json.dump(downloaded, f)
