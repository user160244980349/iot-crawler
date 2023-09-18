import json
import logging
import os
from hashlib import md5
from multiprocessing import Pool
from selenium.common.exceptions import WebDriverException

import config
from crawler.modules.module import Module
from crawler.product import Product
from crawler.web.driver import Driver
from tools.text import url_to_name


class Downloader(Module):

    def __init__(self, policies_json, explicit_json, downloaded_json,
                 original_policies, cooldown=0., random_cooldown=0.):

        super(Downloader, self).__init__()

        self.policies_json = policies_json
        self.explicit_json = explicit_json
        self.downloaded_json = downloaded_json
        self.original_policies = original_policies
        self.cooldown = cooldown
        self.random_cooldown = random_cooldown

    def run_(self, *args, **kwargs):
        """
        In case of missing downloaded.json file
        1. Read list of urls
        2. Turn them to filenames
        3. Process them by 1 and check file existence
        4. If the file exists assign it in the record
        5. Write the results
        """
        for i, r in enumerate(self.records):
            name = url_to_name(r['policy'])
            path = os.path.relpath(os.path.join(self.original_policies, name))
            if os.path.isfile(path):
                self.records[i]["original_policy"] = os.path.join(self.original_policies, name)

                with open(path, 'r') as f:
                    content = f.read()
                    self.records[i]['policy_hash'] = md5(content.encode()).hexdigest()

    def run(self, p: Pool = None):
        self.logger.info("Download")

        jobs = filter(None, set(r["policy"] for r in self.records))

        downloaded = [self.get_policy(j) for j in jobs] \
            if p is None else p.map(self.get_policy, jobs)

        for item in self.records:
            for policy, policy_path, policy_hash in downloaded:
                if policy == item["policy"]:
                    item["original_policy"] = policy_path
                    item["policy_hash"] = policy_hash

    def bootstrap(self):

        with open(os.path.abspath(self.policies_json), "r") as f:
            self.records.extend(json.load(f))

        with open(os.path.abspath(self.explicit_json), "r") as f:
            explicit = json.load(f)
            Product.counter = len(self.records)
            explicit = [Product(**item) for item in explicit]
            self.records.extend(explicit)

    def finish(self):
        with open(os.path.relpath(self.downloaded_json), "w") as f:
            json.dump(self.records, f, indent=2)

    def get_policy(self, policy_url):
        logger = logging.getLogger(f"pid={os.getpid()}")

        driver = Driver()
        net_error = 0

        while True:
            logger.info(f"Getting for policy to {policy_url}")
            try:
                driver.get(policy_url, remove_invisible=True)
                markup = driver.source()
                break

            except WebDriverException:
                logger.warning(f"Web driver exception, potentially net error")
                driver.change_proxy()
                net_error += 1
                if net_error > config.max_error_attempts:
                    return policy_url, None, None

        policy = os.path.abspath(os.path.join(self.original_policies,
                                              url_to_name(policy_url)))

        with open(policy, "w", encoding="utf-8") as f:
            f.write(markup)

        return policy_url, policy, md5(markup.encode()).hexdigest()

