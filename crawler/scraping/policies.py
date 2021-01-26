import json
import logging
import os
import re
from multiprocessing import Pool

from bs4 import BeautifulSoup

from config import resources, websites_json, policies_json
from crawler.web.driver import Driver


def scrap_policies(item):
    driver = Driver()
    markup = driver.get(item["website"], delayed=True)
    soup = BeautifulSoup(markup, "html.parser").find("body")
    refs = soup.findAll('a')

    item["policy"] = None

    for r in reversed(refs):
        if re.match(r"Privacy Policy", r.text) is not None:

            if re.match(r"^.*\.(com|org|eu).*$", r.get('href')) is not None:
                pattern = rf"(^http://|^https://|www\.|//)"
                item["policy"] = f"https://{re.sub(pattern, '', r.get('href'))}"
                return item

            pattern = rf"(^/|/$|//)"
            item["policy"] = f"{item['website']}/{re.sub(pattern, '', r.get('href'))}"
            return item

    for r in reversed(refs):
        if re.match(r"Privacy", r.text) is not None:

            if re.match(r"^.*\.(com|org|eu).*$", r.get('href')) is not None:
                pattern = rf"(^http://|^https://|www\.|//)"
                item["policy"] = f"https://{re.sub(pattern, '', r.get('href'))}"
                return item

            pattern = rf"(^/|/$|//)"
            item["policy"] = f"{item['website']}/{re.sub(pattern, '', r.get('href'))}"
            return item

    return item


def policies(p: Pool):
    logger = logging.getLogger(f"Main process")
    logger.info("Searching policies")

    with open(os.path.join(resources, websites_json), "r") as f:
        websites = json.load(f)

    privacy_policies = p.map(scrap_policies, websites)

    with open(os.path.join(resources, policies_json), "w") as f:
        json.dump(privacy_policies, f)
