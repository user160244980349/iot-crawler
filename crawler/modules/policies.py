import json
import logging
import os
import re
from multiprocessing import Pool

from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException

import config
from crawler.modules.module import Module
from crawler.web.driver import Driver


class Policies(Module):

    def __init__(self):
        super(Policies, self).__init__()
        self.logger = logging.getLogger(f"pid={os.getpid()}")

        self.templates = (
            Policies.template1,
            Policies.template2
        )

    def run(self, p: Pool = None):
        self.logger.info("Searching policies")

        if p is None:
            privacy_policies = [self.scrap_policies_urls(i) for i in set([it["website"] for it in self.records])]
        else:
            privacy_policies = p.map(self.scrap_policies_urls, set([it["website"] for it in self.records]))

        for item in self.records:
            for website, policy in privacy_policies:
                if website == item["website"]:
                    item["policy"] = policy

    def bootstrap(self):
        with open(os.path.abspath(config.websites_json), "r") as f:
            self.records = json.load(f)

    def finish(self):
        with open(os.path.abspath(config.policies_json), "w") as f:
            json.dump(self.records, f, indent=2)

    def scrap_policies_urls(self, website_url):
        return self.scrap_policies_urls_base(
            website_url,
            (self.template1, self.template2),
        )

    @classmethod
    def template1(cls, website, soup):
        refs = soup.findAll("a")

        for r in reversed(refs):
            if r.text is not None and re.match(r"Privacy Policy", r.text):

                if r.get("href") is not None:
                    pattern = rf"(^http://|^https://|www\.|//)"
                    return f"https://{re.sub(pattern, '', r.get('href'))}"

                pattern = rf"(^/|/$|//)"
                return f"{website}/{re.sub(pattern, '', r.get('href'))}"

    @classmethod
    def template2(cls, website, soup):
        refs = soup.findAll("a")

        for r in reversed(refs):
            if r.text is not None and re.match(r"Privacy", r.text):
                if r.get("href") is not None:
                    pattern = rf"(^http://|^https://|www\.|//)"
                    return f"https://{re.sub(pattern, '', r.get('href'))}"

                pattern = rf"(^/|/$|//)"
                return f"{website}/{re.sub(pattern, '', r.get('href'))}"

    @classmethod
    def scrap_policies_urls_base(cls, website_url, templates):
        if website_url is None:
            return website_url, None

        logger = logging.getLogger(f"pid={os.getpid()}")
        driver = Driver()

        net_error = 0

        while True:
            logger.info(f"Getting for policy to {website_url}")
            try:
                markup = driver.get(website_url)
                break

            except WebDriverException:
                logger.warning(f"Web driver exception, potentially net error")
                driver.change_proxy()
                net_error += 1
                if net_error > config.max_error_attempts:
                    return website_url, None

        soup = BeautifulSoup(markup, "lxml").find("body")

        for t in templates:
            policy_url = t(website_url, soup)
            if policy_url is not None:
                break

        return website_url, policy_url
