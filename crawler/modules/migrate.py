import json
import logging
import shutil
from distutils.dir_util import copy_tree
from multiprocessing import Pool

import os

import config
from crawler.modules.module import Module


class Migrate(Module):

    def bootstrap(self):
        pass

    def finish(self):
        pass

    def run(self, p: Pool = None):

        try:
            if not os.path.exists(config.deploy_abs):
                os.makedirs(config.deploy_abs)

            shutil.copyfile(config.plain_json, os.path.join(config.deploy_abs, "plain.json"))

            with open(os.path.abspath(os.path.join(config.deploy_abs, "plain.json")), "r") as f:
                self.records.extend(json.load(f))
                for r in self.records:
                    r["original_policy"] = None
                    r["processed_policy"] = None
                    if r["plain_policy"] is not None:
                        r["plain_policy"] = os.path.join("plain_policies", r["plain_policy"].split('\\')[-1:][0])

            with open(os.path.abspath(os.path.join(config.deploy_abs, "plain.json")), "w") as f:
                json.dump(self.records, f, indent=2)

            copy_tree(config.plain_policies, os.path.join(config.deploy_abs, "plain_policies"))
            shutil.make_archive("../iot-dataset", "zip", os.path.abspath(config.deploy_abs))

        except Exception as e:
            print(e)
