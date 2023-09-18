import logging
import os
import re

from bs4 import BeautifulSoup


class LinkMatcher:
    href = re.compile(r"^((http(s)?:\/\/)(www\.)?([\w\.\-_]+)?)?(\/.*)$")
    http = re.compile(r"(https?:(\/\/)?)")

    def __init__(self, privacy_links):
        self.logger = logging.getLogger(f"pid={os.getpid()}")

        privacy_links = [pl.replace(" ", ".*") for pl in privacy_links]
        self.regexes = [re.compile(pl) for pl in privacy_links]
        self.templates = [self.template1]

    def match(self, website, soup):
        for t in self.templates:
            if policy_url := t(website, soup):
                return policy_url

    def template1(self, website, markup):
        try:
            soup = BeautifulSoup(markup, "lxml").find("body")
            links = soup.findAll("a")
            for link in links:
                if any((reg.match(link.text.lower()) for reg in self.regexes)):
                    if ref := self.href.match(link.get("href")):
                        if ref.group(1):
                            return ref.group(0)
                        else:
                            return f"{website}{ref.group(6)}"

        except Exception:
            pass
