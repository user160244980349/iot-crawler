import json
import logging
import os
import re
from multiprocessing import Pool

from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException

import config
from config import resources, websites_json, policies_json
from crawler.web.driver import Driver


def template1(website, soup):
    refs = soup.findAll("a")

    for r in reversed(refs):
        if r.text is not None and re.match(r"Privacy Policy", r.text):

            if r.get('href') is not None \
                    and re.match(r"^.*\.(com|org|eu).*$", r.get('href')) is not None:
                pattern = rf"(^http://|^https://|www\.|//)"
                return f"https://{re.sub(pattern, '', r.get('href'))}"

            pattern = rf"(^/|/$|//)"
            return f"{website}/{re.sub(pattern, '', r.get('href'))}"


def template2(website, soup):
    refs = soup.findAll("a")

    for r in reversed(refs):
        if r.text is not None and re.match(r"Privacy", r.text):

            if r.get("href") is not None \
                    and re.match(r"^.*\.(com|org|eu).*$", r.get("href")) is not None:
                pattern = rf"(^http://|^https://|www\.|//)"
                return f"https://{re.sub(pattern, '', r.get('href'))}"

            pattern = rf"(^/|/$|//)"
            return f"{website}/{re.sub(pattern, '', r.get('href'))}"


templates = [
    template1,
    template2,
]


def policies(p: Pool):
    logger = logging.getLogger(f"pid={os.getpid()}")
    logger.info("Searching policies")

    with open(os.path.join(resources, config.websites_json), "r") as f:
        items = json.load(f)

    privacy_policies = p.map(scrap_policies_urls, set([it["website"] for it in items]))

    for item in items:
        for website, policy in privacy_policies:
            if website == item["website"]:
                item["policy"] = policy

    with open(os.path.join(resources, policies_json), "w") as f:
        json.dump(items, f)


def scrap_policies_urls(website_url):
    if website_url is None:
        return website_url, None

    logger = logging.getLogger(f"pid={os.getpid()}")
    driver = Driver()
    net_error = 0
    while True:
        logger.warning(f"Getting for policy to {website_url}")
        try:
            markup = driver.get(website_url)
            break

        except WebDriverException as e:
            logger.warning(f"Web driver exception, potentially net error")
            driver.change_proxy()
            net_error += 1
            if net_error > config.max_error_attempts:
                return website_url, None

    soup = BeautifulSoup(markup, "lxml").find("body")

    policy_url = None
    for t in templates:
        policy_url = t(website_url, soup)
        if policy_url is not None:
            break

    return website_url, policy_url
