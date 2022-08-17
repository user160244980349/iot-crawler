import json
import logging
import os
from pprint import pprint
from multiprocessing import Pool

from bs4 import BeautifulSoup

import config
from crawler.modules.module import Module


class Efficiency(Module):

    h = 0
    p = 0
    li = 0
    ol = 0
    ul = 0
    table = 0

    def __init__(self,
                 pj=config.plain_json,
                 mj=config.metrics_json):
        super(Efficiency, self).__init__()
        self.logger = logging.getLogger(f"pid={os.getpid()}")

        self.plain_json = pj
        self.metrics_json = mj

        self.metrics = {
            "items_total": 0,
            "products": {
                "manufacturers": 0,
                "websites": 0,
                "policies": 0,
                "percentile_manufacturers": 0.,
                "percentile_websites": 0.,
                "percentile_policies": 0.,
            },
            "unique": {
                "manufacturers": 0,
                "websites": 0,
                "policies": 0,
                "percentile_manufacturers": 0.,
                "percentile_websites": 0.,
                "percentile_policies": 0.,
            }
        }

    def run(self, p: Pool = None):
        self.logger.info("Efficiency calculation")

        self.metrics["items_total"] = len(self.records)
        self.products_statistics()
        self.websites_statistics()

        jobs = [r for r in self.records if None not in (r["original_policy"],
                                                        r["processed_policy"],
                                                        r["plain_policy"])]

        results = [self.policy_statistics(j) for j in jobs] \
            if p is None else p.map(self.policy_statistics, jobs)

        for item in self.records:
            for stats, original_policy in results:
                if original_policy == item["original_policy"]:
                    item["statistics"] = stats

        h = 0
        p = 0
        li = 0
        ol = 0
        ul = 0
        table = 0

        for item in {r[1]: r[0] for r in results}.values():
            h += item["headings"]
            p += item["paragraphs"]
            li += item["list items"]
            ol += item["ordered lists"]
            ul += item["unordered lists"]
            table += item["tables"]

        print(f"h {h / 592}")
        print(f"p {p / 592}")
        print(f"li {li / 592}")
        print(f"ol {ol / 592}")
        print(f"ul {ul / 592}")
        print(f"table {table / 592}")

    def bootstrap(self):
        with open(os.path.abspath(self.plain_json), "r", encoding="utf-8") as f:
            self.records = json.load(f)

    def finish(self):
        with open(os.path.abspath(self.plain_json), "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=2)

        with open(os.path.abspath(self.metrics_json), "w", encoding="utf-8") as f:
            json.dump(self.metrics, f, indent=2)

    def products_statistics(self):
        manufacturers = [item["manufacturer"]
                         for item in self.records if item["manufacturer"] is not None]
        websites = [item["website"] for item in self.records if item["website"] is not None]
        policies = [item["policy"] for item in self.records if item["policy"] is not None]

        self.metrics["products"]["manufacturers"] = len(manufacturers)
        self.metrics["products"]["websites"] = len(websites)
        self.metrics["products"]["policies"] = len(policies)

        self.metrics["products"]["percentile_manufacturers"] = \
            self.metrics["products"]["manufacturers"] / self.metrics["items_total"]
        self.metrics["products"]["percentile_websites"] = \
            self.metrics["products"]["websites"] / self.metrics["items_total"]
        self.metrics["products"]["percentile_policies"] = \
            self.metrics["products"]["policies"] / self.metrics["items_total"]

    def websites_statistics(self):
        manufacturers = [item["manufacturer"]
                         for item in self.records if item["manufacturer"] is not None]
        websites = [item["website"] for item in self.records if item["website"] is not None]
        hashes = [item["policy_hash"] for item in self.records if item["policy_hash"] is not None]

        self.metrics["unique"]["manufacturers"] = len(set(manufacturers))
        self.metrics["unique"]["websites"] = len(set(websites))
        self.metrics["unique"]["policies"] = len(set(hashes))

        self.metrics["unique"]["percentile_manufacturers"] = \
            self.metrics["unique"]["manufacturers"] / self.metrics["products"]["manufacturers"]
        self.metrics["unique"]["percentile_websites"] = \
            self.metrics["unique"]["websites"] / self.metrics["unique"]["manufacturers"]
        self.metrics["unique"]["percentile_policies"] = \
            self.metrics["unique"]["policies"] / self.metrics["unique"]["manufacturers"]

    @classmethod
    def policy_statistics(cls, product):

        with open(os.path.abspath(product["original_policy"]), "r", encoding="utf-8") as f:
            original_policy = BeautifulSoup(f.read(), "lxml")

        with open(os.path.abspath(product["processed_policy"]), "r", encoding="utf-8") as f:
            sanitized_policy = BeautifulSoup(f.read(), "lxml")

        with open(os.path.abspath(product["plain_policy"]), "r", encoding="utf-8") as f:
            plain_policy = f.read()

        paragraphs = plain_policy.split("\n")
        paragraphs = [p for p in paragraphs if p != ""]
        pars, heads = cls.count_headings(paragraphs)

        return {
                   "length": len(str(sanitized_policy)),
                   "list items": len(sanitized_policy.findAll("li")),
                   "ordered lists": len(sanitized_policy.findAll("ol")),
                   "unordered lists": len(sanitized_policy.findAll("ul")),
                   "tables": len(original_policy.findAll("table")),
                   "paragraphs": pars,
                   "headings": heads,
               }, product["original_policy"]

    @staticmethod
    def count_headings(paragraphs):
        pars, heads = 0, 0

        stack = 0

        import re
        for p in paragraphs:

            if re.match(r"(\{list item\})", p) is None and stack > 0:
                stack -= 1

            if re.match(r"(\{number list\})|(\{bullet list\})", p) is not None:
                stack += 1
                continue

            if stack == 0:
                if len(p) < 100:
                    heads += 1
                else:
                    pars += 1

        return pars, heads
