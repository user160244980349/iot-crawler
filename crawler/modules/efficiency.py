import json
import logging
import os
from multiprocessing import Pool

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

    def bootstrap(self):
        with open(os.path.abspath(config.sanitized_json), "r") as f:
            self.records = json.load(f)

    def finish(self):
        with open(os.path.abspath(config.metrics_json), "w") as f:
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
