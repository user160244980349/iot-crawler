import json
import logging
import os
import re
from multiprocessing import Pool

from bs4 import BeautifulSoup
from html_sanitizer import Sanitizer

import config
from crawler.modules.module import Module
from tools.arrays import flatten_list


class Sanitization(Module):
    words = [
        "head", "cart", "foot", "nav", "bar",
        "alert", "modal", "popup",
        "banner", "promo", "side", "notify",
        "notification", "toolbar", "menu",
        "ft", "hd", "navigation", "shopify",
        "footer", "header"
    ]

    tags = [
        # "select", "option", "button", "style", "script", "form"
    ]

    indentation = re.compile(r'^(\s*)', re.MULTILINE)
    split_html_attrs = re.compile(r"\W")

    def __init__(self,
                 dj=config.downloaded_json,
                 sj=config.sanitized_json,
                 pp=config.processed_policies,
                 sc=config.sanitizer_settings):

        super(Sanitization, self).__init__()
        self.logger = logging.getLogger(f"pid={os.getpid()}")

        self.downloaded_json = dj
        self.sanitized_json = sj
        self.processed_policies = pp
        self.sanitizer_settings = sc

    def run(self, p: Pool = None):

        self.logger.info("Sanitization")

        jobs = filter(None, set([r["original_policy"] for r in self.records]))

        sanitized = [self.clean_webpage(j) for j in jobs] \
            if p is None else p.map(self.clean_webpage, jobs)

        for item in self.records:
            for policy, sanitized_policy in sanitized:
                if policy == item["original_policy"]:
                    item["processed_policy"] = sanitized_policy

    def bootstrap(self):
        with open(os.path.abspath(self.downloaded_json), "r") as f:
            self.records.extend(json.load(f))

    def finish(self):
        with open(os.path.abspath(self.sanitized_json), "w") as f:
            json.dump(self.records, f, indent=2)

    def clean_webpage(self, item):

        if item is None:
            return item, None, None

        with open(item, "r", encoding="utf-8") as input_f:
            html = input_f.read()

        soup = BeautifulSoup(html, "lxml")

        self.bs4_aggressive_remove(soup)

        sanitized = Sanitizer(settings=self.sanitizer_settings).sanitize(str(soup))
        fresh_soup = BeautifulSoup(sanitized, "lxml")

        sanitized_policy = os.path.abspath(
            os.path.join(self.processed_policies, os.path.basename(item))
        )

        with open(sanitized_policy, "w", encoding="utf-8") as output_f:
            output_f.write(f"<html>\n"
                           f"<head>\n"
                           f"\t<meta charset=\"utf-8\"/>\n"
                           f"\t<title></title>\n"
                           f"</head>\n"
                           f"{self.prettify(fresh_soup.body)}\n"
                           f"</html>")

        return item, sanitized_policy

    @classmethod
    def bs4_aggressive_remove(cls, element):

        try:
            s = list(element.get("class"))
        except TypeError:
            s = []

        id_ = element.get("id")
        if id_ is not None:
            s.append(id_)

        if element.name is not None:
            s.append(element.name)

        s = flatten_list([cls.split_html_attrs.split(st.lower()) for st in s])
        m = [i in cls.words for i in s]

        if (True in m or element.name in cls.tags) \
                and element.name not in ("html", "body", "title", "head"):
            cls.remove_tags(element)
            element.extract()
            return

        for child in element.findAll(recursive=False):
            cls.bs4_aggressive_remove(child)

    @classmethod
    def prettify(cls, soup, indent_width=4):
        try:
            return cls.indentation.sub(r"\1" * indent_width, soup.prettify())
        except (AttributeError, ValueError):
            return ""

    @classmethod
    def remove_tags(cls, soup, **kwargs):
        for e in soup.findAll(**kwargs):
            e.extract()
