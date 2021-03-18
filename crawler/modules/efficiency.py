import json
import logging
import os
from multiprocessing import Pool

from bs4 import BeautifulSoup

import config
from crawler.modules.module import Module


class Efficiency(Module):

    def __init__(self):
        super(Efficiency, self).__init__()
        self.logger = logging.getLogger(f"pid={os.getpid()}")

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

    def bootstrap(self):
        with open(os.path.abspath(config.plain_json), "r", encoding="utf-8") as f:
            self.records = json.load(f)

    def finish(self):
        with open(os.path.abspath(config.plain_json), "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=2)

        with open(os.path.abspath(config.metrics_json), "w", encoding="utf-8") as f:
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

    @staticmethod
    def policy_statistics(product):

        with open(os.path.abspath(product["original_policy"]), "r", encoding="utf-8") as f:
            original_policy = BeautifulSoup(f.read(), "lxml")

        with open(os.path.abspath(product["processed_policy"]), "r", encoding="utf-8") as f:
            sanitized_policy = BeautifulSoup(f.read(), "lxml")

        return {
                   "length": len(str(sanitized_policy)),
                   "table": len(original_policy.findAll("table")),
                   "ol": len(sanitized_policy.findAll("ol")),
                   "ul": len(sanitized_policy.findAll("ul")),
                   "li": len(sanitized_policy.findAll("li")),
                   "p": len(sanitized_policy.findAll("p")),
                   "br": len(sanitized_policy.findAll("br")),
               }, product["original_policy"]
