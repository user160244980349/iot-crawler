import json
import logging
import os
from multiprocessing import Pool

from bs4 import BeautifulSoup
from html_sanitizer import Sanitizer

import config
from sanitizer.html_sanitizer_functions import remove_tags


def clean(p: Pool):
    logger = logging.getLogger(f"pid={os.getpid()}")
    logger.info("Sanitization")

    with open(os.path.join(config.resources, config.downloaded_json), "r") as f:
        items = json.load(f)

    sanitized = p.map(clean_webpage, set(i["original_policy"] for i in items))

    for item in items:
        for policy, sanitized_policy, stats in sanitized:
            if policy == item["original_policy"]:
                item["processed_policy"] = sanitized_policy
                item["statistics"] = stats

    with open(os.path.join(config.resources, config.sanitized_json), "w") as f:
        json.dump(items, f)


def clean_webpage(item):
    if item is None:
        return item, None, None

    with open(item, "r", encoding="utf-8") as input_f:
        html = input_f.read()

        soup = BeautifulSoup(html, "lxml")

        remove_tags(soup, "head")
        remove_tags(soup, "a")
        remove_tags(soup, "title")

        sanitized_policy = os.path.join(config.resources, config.processed_policies,
                                        os.path.basename(item))
        sanitized = Sanitizer(settings=config.sanitizer_settings).sanitize(str(soup))

        fresh_soup = BeautifulSoup(html, "lxml")
        stats = {
            "length": len(sanitized),
            "ol": len(fresh_soup.find_all("ol")),
            "ul": len(fresh_soup.find_all("ul")),
            "li": len(fresh_soup.find_all("li")),
            "p": len(fresh_soup.find_all("p")),
            "br": len(fresh_soup.find_all("br")),
        }

        with open(sanitized_policy, "w", encoding="utf-8") as output_f:
            output_f.write(f"<html>"
                           f"<head>"
                           f"<meta charset='utf-8'/>"
                           f"<title></title>"
                           f"</head>"
                           f"<body>"
                           f"{sanitized}"
                           f"</body>"
                           f"</html>")

        return item, sanitized_policy, stats
