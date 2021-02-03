import json
import logging
import os
from hashlib import md5
from multiprocessing import Pool
from os import getpid
from os.path import join

from selenium.common.exceptions import WebDriverException

import config
from config import original_policies, resources, policies_json, downloaded_json
from crawler.web.driver import Driver
from tools.text import url_to_name


def download(p: Pool):
    logger = logging.getLogger(f"pid={getpid()}")
    logger.info("Download")

    with open(os.path.join(resources, policies_json), "r") as f:
        items = json.load(f)

    downloaded = p.map(get_policy, set(i["policy"] for i in items))

    for item in items:
        for policy, policy_path, policy_hash in downloaded:
            if policy == item["policy"]:
                item["original_policy"] = policy_path
                item["policy_hash"] = policy_hash

    with open(os.path.join(resources, downloaded_json), "w") as f:
        json.dump(items, f)


def get_policy(policy_url):
    if policy_url is None:
        return policy_url, None, None

    logger = logging.getLogger(f"pid={os.getpid()}")

    driver = Driver()
    net_error = 0
    while True:
        logger.warning(f"Getting for policy to {policy_url}")
        try:
            markup = driver.get(policy_url)
            break

        except WebDriverException as e:
            logger.warning(f"Web driver exception, potentially net error")
            driver.change_proxy()
            net_error += 1
            if net_error > config.max_error_attempts:
                return policy_url, None, None

    policy = join(resources, original_policies, url_to_name(policy_url))

    with open(policy, "w", encoding="utf-8") as f:
        f.write(markup)

    return policy_url, policy, md5(markup.encode()).hexdigest()
