import json
import shutil
from distutils.dir_util import copy_tree
from multiprocessing import Pool

import os

from config import deploy_abs, plain_json, plain_policies
from crawler.modules.module import Module


class Pack(Module):

    def bootstrap(self):
        pass

    def finish(self):
        pass

    def run(self, p: Pool = None):

        if not os.path.exists(deploy_abs):
            os.makedirs(deploy_abs)

        shutil.copyfile(plain_json, os.path.join(deploy_abs, "plain.json"))

        with open(os.path.abspath(os.path.join(deploy_abs, "plain.json")), "r") as f:
            self.records.extend(json.load(f))
            self.records = [Pack.process_record(r) for r in self.records]

        with open(os.path.abspath(os.path.join(deploy_abs, "plain.json")), "w") as f:
            json.dump(self.records, f, indent=2)

        copy_tree(plain_policies, os.path.join(deploy_abs, "plain_policies"))
        shutil.make_archive("../iot-dataset", "zip", os.path.abspath(deploy_abs))

    @classmethod
    def process_record(cls, record):
        new = {
            "id": record["id"],
            "url": record["url"],
            "manufacturer": record["manufacturer"],
            "keyword": record["keyword"],
            "website": record["website"],
            "policy": record["policy"],
            "plain_policy": record["plain_policy"],
            "policy_hash": record["policy_hash"],
        }

        return new
