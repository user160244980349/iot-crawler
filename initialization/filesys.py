import os
import json

import config


def init():

    if not is_locked(config.lockfile):

        if not os.path.exists(config.resources_abs):
            os.makedirs(config.resources_abs)
            os.makedirs(os.path.join(config.resources_abs, "json"))
            os.makedirs(config.original_policies)
            os.makedirs(config.processed_policies)
            os.makedirs(config.plain_policies)

        if not os.path.exists(config.mail_ru_top_abs):
            os.makedirs(config.mail_ru_top_abs)
            os.makedirs(os.path.join(config.mail_ru_top_abs, "json"))
            os.makedirs(config.mrt_original_policies)
            os.makedirs(config.mrt_processed_policies)
            os.makedirs(config.mrt_plain_policies)

        with open(os.path.abspath(config.explicit_json), "w", encoding="utf-8") as f:
            json.dump([
                {
                    "manufacturer": "xiaomi",
                    "website": "https://mi.com/global/",
                    "policy": "https://mi.com/global/about/privacy/"
                }
            ], f, indent=2)

        with open(os.path.abspath(config.mrt_explicit), "w", encoding="utf-8") as f:
            json.dump([
                {
                    "website": "https://mi.com/global/",
                    "policy": "https://mi.com/global/about/privacy/"
                }
            ], f, indent=2)

        lock(config.lockfile)


def is_locked(path):
    if os.path.isfile(path):
        return True
    else:
        return False


def lock(path):
    f = open(path, 'w')
    f.close()
