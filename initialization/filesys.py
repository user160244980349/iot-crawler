import os
import json

import config


def init():
    json_folder = os.path.join(config.resources_abs, "json")
    op = os.path.abspath(config.original_policies)
    pp = os.path.abspath(config.processed_policies)
    plp = os.path.abspath(config.plain_policies)

    if not os.path.exists(config.resources_abs):
        os.makedirs(config.resources_abs)

    if not os.path.exists(json_folder):
        os.makedirs(json_folder)

    if not os.path.exists(op):
        os.makedirs(op)

    if not os.path.exists(pp):
        os.makedirs(pp)

    if not os.path.exists(plp):
        os.makedirs(plp)

    with open(os.path.abspath(config.products_json), "w", encoding="utf-8") as f:
        json.dump(list(), f, indent=2)

    with open(os.path.abspath(config.websites_json), "w", encoding="utf-8") as f:
        json.dump(list(), f, indent=2)

    with open(os.path.abspath(config.policies_json), "w", encoding="utf-8") as f:
        json.dump(list(), f, indent=2)

    with open(os.path.abspath(config.downloaded_json), "w", encoding="utf-8") as f:
        json.dump(list(), f, indent=2)

    with open(os.path.abspath(config.sanitized_json), "w", encoding="utf-8") as f:
        json.dump(list(), f, indent=2)

    with open(os.path.abspath(config.converted_json), "w", encoding="utf-8") as f:
        json.dump(list(), f, indent=2)

    with open(os.path.abspath(config.plain_json), "w", encoding="utf-8") as f:
        json.dump(list(), f, indent=2)

    with open(os.path.abspath(config.explicit_json), "w", encoding="utf-8") as f:
        json.dump([
            {
                "manufacturer": "xiaomi",
                "website": "https://mi.com/global/",
                "policy": "https://mi.com/global/about/privacy/"
            }
        ], f, indent=2)

    with open(os.path.abspath(config.metrics_json), "w", encoding="utf-8") as f:
        json.dump(list(), f, indent=2)
