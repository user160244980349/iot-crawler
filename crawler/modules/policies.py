import json
import logging
import os
import re
from multiprocessing import Pool

import config
from crawler.modules.module import Module
from crawler.web.driver import Driver
from tools.hashable_dict import HashableDict

from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup


def split_data(data, chunks):
    ld = len(data)
    return [[data[i] for i in range(ch, ld, chunks)] for ch in range(chunks)]


def _count_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)


def get_file_size(file):
    size = 0
    try:
        with open(file, 'rb') as fp:
            c_generator = _count_generator(fp.raw.read)
            size = sum(buffer.count(b'\n') for buffer in c_generator)
    except FileNotFoundError:
        pass
    return size


class Policies(Module):
    sanitize_a = re.compile(r"[^\w]")
    privacy_link = re.compile(r"privacy(policy)?")
    href = re.compile(r"^((https?://)?(www\.)?([\w.\-_]+)\.\w+)?(.*$)")
    http = re.compile("(https?:(//)?)")

    def __init__(self, websites_json, policies_json, link_matcher):

        super(Policies, self).__init__()

        self.link_matcher = link_matcher
        self.websites_json = websites_json
        self.policies_json = policies_json

    def run(self, p: Pool = None):
        self.logger.info("Searching policies")

        jobs = filter(None, set([r["website"] for r in self.records]))

        privacy_policies = [self.scrap_policies_urls(j) for j in jobs] \
            if p is None else p.map(self.scrap_policies_urls, jobs)

        for item in self.records:
            for website, policy in privacy_policies:
                if website == item["website"]:
                    item["policy"] = policy

    def bootstrap(self):
        with open(os.path.relpath(self.websites_json), "r") as f:
            self.records = json.load(f)
            self.records = [HashableDict(r) for r in self.records]

    def finish(self):
        with open(os.path.relpath(self.policies_json), "w") as f:
            json.dump(self.records, f, indent=2)

    def scrap_policies_urls(self, website_url):
        return self.scrap_policies_urls_base(
            website_url,
            (self.template1,),
        )

    def template1(self, website, soup):
        try:
            refs = soup.findAll("a")
            for r in reversed(refs):
                if self.privacy_link.match(self.sanitize_a.sub("", r.text.lower())):

                    m = self.href.match(r.get("href"))
                    if m is not None:
                        return f"http://{self.http.sub('', website)}{m.group(5)}"

        except (AttributeError, TypeError):
            self.logger.error("Policy is not found")

    @classmethod
    def scrap_policies_urls_base(cls, website_url, templates):

        logger = logging.getLogger(f"pid={os.getpid()}")
        driver = Driver()

        net_error = 0
        policy_url = None

        markup = None
        while True:
            logger.info(f"Getting for policy to {website_url}")
            try:
                driver.get(website_url)
                markup = driver.source()
                break

            except WebDriverException:
                logger.warning(f"Web driver exception, potentially net error")

                driver.change_proxy()
                driver.restart_session()

                net_error += 1
                if net_error > config.max_error_attempts:
                    return website_url, policy_url
        
        soup = BeautifulSoup(markup, "lxml").find("body")

        for t in templates:
            policy_url = t(website_url, soup)
            if policy_url is not None:
                break

        return website_url, policy_url