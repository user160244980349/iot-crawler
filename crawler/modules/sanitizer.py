import json
import logging
import os
import re
from multiprocessing import Pool

from bs4 import BeautifulSoup
from html_sanitizer import Sanitizer

import config
from crawler.modules.module import Module


class Sanitization(Module):

    words = [
        "head", "cart", "foot", "nav", "bar",
        "alert", "modal", "dialog", "popup",
        "banner", "promo", "side"
    ]

    tags = [
        "select", "option", "button", "style", "script", "a",
        # "head", "title",
    ]

    regex = re.compile(rf"^.*({'|'.join(words)}).*$", flags=re.IGNORECASE)

    def __init__(self):
        super(Sanitization, self).__init__()
        self.logger = logging.getLogger(f"pid={os.getpid()}")

    def run(self, p: Pool = None):
        self.logger.info("Sanitization")

        if p is None:
            sanitized = [self.clean_webpage(i) for i in set([r["original_policy"] for r in self.records])]
        else:
            sanitized = p.map(self.clean_webpage, set(r["original_policy"] for r in self.records))

        for item in self.records:
            for policy, sanitized_policy, stats in sanitized:
                if policy == item["original_policy"]:
                    item["processed_policy"] = sanitized_policy
                    item["statistics"] = stats

    def bootstrap(self):
        with open(os.path.abspath(config.downloaded_json), "r") as f:
            self.records.extend(json.load(f))

    def finish(self):
        with open(os.path.abspath(config.sanitized_json), "w") as f:
            json.dump(self.records, f, indent=2)

    @classmethod
    def clean_webpage(cls, item):
        if item is None:
            return item, None, None

        with open(item, "r", encoding="utf-8") as input_f:
            html = input_f.read()

        soup = BeautifulSoup(html, "lxml")

        for n in cls.tags:
            cls.remove_tags(soup, name=n)

        cls.bs4_remover(soup)
        sanitized = Sanitizer(settings=config.sanitizer_settings).sanitize(str(soup))
        fresh_soup = BeautifulSoup(sanitized, "lxml")

        stats = {
            "length": len(str(fresh_soup)),
            "table": len(soup.find_all("table")),
            "ol": len(fresh_soup.find_all("ol")),
            "ul": len(fresh_soup.find_all("ul")),
            "li": len(fresh_soup.find_all("li")),
            "p": len(fresh_soup.find_all("p")),
            "br": len(fresh_soup.find_all("br")),
        }

        sanitized_policy = os.path.join(config.processed_policies, os.path.basename(item))
        with open(sanitized_policy, "w", encoding="utf-8") as output_f:
            output_f.write(f"<html>"
                           f"<head>"
                           f"<meta charset='utf-8'/>"
                           f"<title></title>"
                           f"</head>"
                           f"{fresh_soup.body.prettify()}"
                           f"</html>")

        return item, sanitized_policy, stats

    @classmethod
    def bs4_remover(cls, element):

        try:
            s = list(element.get("class"))
        except TypeError:
            s = []

        s.append(element.get("id"))
        s.append(element.name)

        m = cls.regex.match(" ".join([i for i in s if i is not None]))

        if m is not None and element.name != "body":
            cls.remove_tags(element)
            element.extract()
            return

        for child in element.find_all(recursive=False):
            cls.bs4_remover(child)

    @classmethod
    def div_to_p(cls, element):
        if element.tag == "div":
            if len(list(element)) == 0:
                element.tag = "p"
        return element

    @classmethod
    def span_to_p(cls, element):
        if element.tag == "span":
            element.tag = "p"
        return element

    @classmethod
    def article_to_div(cls, element):
        if element.tag == "article":
            element.tag = "div"
        return element

    @classmethod
    def remove_tags(cls, soup, **kwargs):
        for e in soup.find_all(**kwargs):
            e.extract()
