import json
from multiprocessing import Pool

import os

from config import downloaded_json, sanitized_json, plain_json
from crawler.modules.module import Module


class FixAbsPaths(Module):
    _keys = ("original_policy", "processed_policy", "plain_policy")
    _files = (downloaded_json, sanitized_json, plain_json)

    def bootstrap(self):
        pass

    def finish(self):
        pass

    def run(self, p: Pool = None):
        for file in self._files:
            with open(os.path.abspath(file), "r") as f:
                self.records = json.load(f)
                self.records = [FixAbsPaths.process_record(r) for r in self.records]

            with open(os.path.abspath(file), "w") as f:
                json.dump(self.records, f, indent=2)

    @classmethod
    def process_record(cls, record):
        for k in cls._keys:
            record[k] = FixAbsPaths.cut_path(record[k]) if record[k] else None
        return record

    @staticmethod
    def cut_path(path):
        return path.split('\\')[-1:][0]