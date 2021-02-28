import json
import logging
import os
import re
from multiprocessing import Pool

from bs4 import BeautifulSoup

import config
from crawler.modules.module import Module


class Converter(Module):

    subs = [
        (r"\n+", ""),         # newlines
        (r"<li>", "** "),        # li_tags
        (r"<ol>", "-- "),     # ol_tags
        (r"</em>", ""),    # em_tags
        (r"</strong>", ""),   # strong_tags
        (r"<\w+>", ""),       # open_tags
        (r"</\w+>", "\n\n"),      # close_tags
        (r"[^A-Za-z0-9,.:\-\n\s()]", ""),  # too_many_ws
        (r"\n{3,}", "\n\n"),  # too_many_nl
        (r"\s{2,}", "\n\n"),  # too_many_ws
    ]

    regexps = [(re.compile(s[0]), s[1]) for s in subs]

    def __init__(self):
        super(Converter, self).__init__()
        self.logger = logging.getLogger(f"pid={os.getpid()}")

    def bootstrap(self):
        with open(os.path.abspath(config.sanitized_json), "r") as f:
            self.records = json.load(f)

    def run(self, p: Pool = None):
        self.logger.info("Converting to plain text")

        if p is None:
            plain = [self.plain_webpage(i) for i in set([r["processed_policy"] for r in self.records])]
        else:
            plain = p.map(self.plain_webpage, set(r["processed_policy"] for r in self.records))

        for item in self.records:
            for policy, plain_policy in plain:
                if policy == item["processed_policy"]:
                    item["plain_policy"] = plain_policy

    def finish(self):
        with open(os.path.abspath(config.plain_json), "w") as f:
            json.dump(self.records, f, indent=2)

    @classmethod
    def plain_webpage(cls, item):

        if item is None:
            return item, None

        with open(os.path.abspath(item), "r", encoding="utf-8") as f:
            text = f.read()

        soup = BeautifulSoup(text, "lxml")
        text = str(soup.body)

        for r in cls.regexps:
            text = r[0].sub(r[1], text)

        policy = os.path.join(os.path.abspath(config.plain_policies), f"{os.path.basename(item)}.txt")
        with open(policy, "w", encoding="utf-8") as f:
            f.write(text)

        return item, policy
