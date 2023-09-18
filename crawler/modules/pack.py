import json
import os
import shutil
from distutils.dir_util import copy_tree
from multiprocessing import Pool
from sys import platform

from crawler.modules.module import Module


class Pack(Module):
    _keys = ("original_policy", "processed_policy", "plain_policy")

    def __init__(self, resources, deploy, downloaded_json,
                 sanitized_json, plain_json, archive):
        super(Pack, self).__init__()

        self._files = (downloaded_json, sanitized_json, plain_json)
        self._resources = resources
        self._deploy = deploy
        self._archive = archive

    def bootstrap(self):
        pass

    def finish(self):
        pass

    def run(self, p: Pool = None):

        if not os.path.exists(self._deploy):
            os.makedirs(self._deploy)
        os.chdir(self._deploy)

        copy_tree(self._resources, os.path.join(self._deploy))

        for file in self._files:
            with open(os.path.relpath(file), "r") as f:
                self.records = json.load(f)
                self.records = [Pack.process_record(r) for r in self.records]

            with open(os.path.relpath(file), "w") as f:
                json.dump(self.records, f, indent=2)

        shutil.make_archive(os.path.join(self._deploy, "..", self._archive),
                            "zip", os.path.relpath(self._deploy))

    @classmethod
    def process_record(cls, record):
        for k in cls._keys:
            record[k] = cls.cut_path(record[k]) if record[k] else None
        return record

    @classmethod
    def cut_path(cls, path):
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            return path.split('/')[-1:][0]
        elif platform == "win32":
            return path.split('\\')[-1:][0]
