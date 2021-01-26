import json
import logging
import os
from multiprocessing import Pool
from os.path import join

from html_sanitizer import Sanitizer

from config import sanitizer_settings, processed_policies, resources, sanitized_json, downloaded_json
from tools.text import url_to_name


def clean_webpage(item):
    item["sanitized_policy"] = None

    if item["original_policy"] is None:
        return item

    with open(item["original_policy"], "r", encoding="utf-8") as input_f:
        html = input_f.read()
        input_f.close()

        item["sanitized_policy"] = join(resources, processed_policies, url_to_name(item["policy"]))

        with open(item["sanitized_policy"], "w", encoding="utf-8") as output_f:
            sanitizer = Sanitizer(sanitizer_settings)
            output_f.write(sanitizer.sanitize(html))
            output_f.close()

    return item


def clean(p: Pool):
    logger = logging.getLogger(f"Main process")
    logger.info("Sanitization")

    with open(os.path.join(resources, downloaded_json), "r") as f:
        downloaded = json.load(f)

    sanitized = p.map(clean_webpage, downloaded)

    with open(os.path.join(resources, sanitized_json), "w") as f:
        json.dump(sanitized, f)
