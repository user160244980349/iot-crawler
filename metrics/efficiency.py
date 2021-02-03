import json
import logging
import os

from config import resources, sanitized_json, total_json


def calculate():
    logger = logging.getLogger(f"pid={os.getpid()}")
    logger.info("Efficiency calculation")

    with open(os.path.join(resources, sanitized_json), "r") as f:
        products = json.load(f)

    metrics = {
        "items_total": len(products),
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

    products_statistics(metrics, products)
    websites_statistics(metrics, products)

    with open(os.path.join(resources, total_json), "w") as f:
        json.dump(metrics, f)


def products_statistics(metrics: dict, items: list):
    manufacturers = [item["manufacturer"]
                     for item in items if item["manufacturer"] is not None]
    websites = [item["website"] for item in items if item["website"] is not None]
    policies = [item["policy"] for item in items if item["policy"] is not None]

    metrics["products"]["manufacturers"] = len(manufacturers)
    metrics["products"]["websites"] = len(websites)
    metrics["products"]["policies"] = len(policies)

    metrics["products"]["percentile_manufacturers"] = \
        metrics["products"]["manufacturers"] / metrics["items_total"]
    metrics["products"]["percentile_websites"] = \
        metrics["products"]["websites"] / metrics["items_total"]
    metrics["products"]["percentile_policies"] = \
        metrics["products"]["policies"] / metrics["items_total"]


def websites_statistics(metrics: dict, items: list):
    manufacturers = [item["manufacturer"]
                     for item in items if item["manufacturer"] is not None]
    websites = [item["website"] for item in items if item["website"] is not None]
    hashes = [item["policy_hash"] for item in items if item["policy_hash"] is not None]

    metrics["unique"]["manufacturers"] = len(set(manufacturers))
    metrics["unique"]["websites"] = len(set(websites))
    metrics["unique"]["policies"] = len(set(hashes))

    metrics["unique"]["percentile_manufacturers"] = \
        metrics["unique"]["manufacturers"] / metrics["products"]["manufacturers"]
    metrics["unique"]["percentile_websites"] = \
        metrics["unique"]["websites"] / metrics["unique"]["manufacturers"]
    metrics["unique"]["percentile_policies"] = \
        metrics["unique"]["policies"] / metrics["unique"]["manufacturers"]
