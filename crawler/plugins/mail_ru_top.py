import json
import logging
import os
import random
import re
from multiprocessing import Pool
from time import sleep

import config
from crawler.plugins.plugin import Plugin
from crawler.web.driver import Driver
from crawler.website import Website
from tools.arrays import flatten_list


class MailRuTop(Plugin):
    captcha_catch = re.compile("sorry, we just need to "
                               "make sure you're not a robot", flags=re.IGNORECASE)

    def __init__(self, keywords, pages,
                 cooldown=0., random_cooldown=0.,
                 captcha_cooldown=0., webdriver_error_cooldown=0.,
                 sync=False):
        super().__init__(keywords, pages, sync)

        self.cooldown = cooldown
        self.random_cooldown = random_cooldown
        self.captcha_cooldown = captcha_cooldown
        self.webdriver_error_cooldown = webdriver_error_cooldown

        self.logger = logging.getLogger(f"pid={os.getpid()}")

    def scrap(self, p: Pool = None):

        Website.counter = len(self.items)

        for keyword in self.keywords:
            search_urls = self.gen_search_urls(keyword, self.pages)

            found_items = flatten_list([self.scrap_websites(url) for url in search_urls] \
                                        if p is None or self.sync else p.map(self.scrap_websites, search_urls))

            websites = [Website(keyword=d[0], website=d[1])
                        for d in [(keyword, item) for item in found_items]]

            self.items.extend(websites)

        with open(os.path.abspath(config.mrt_websites), "w") as f:
            json.dump(self.items, f, indent=2)

    def gen_search_urls(self, keyword, pages):
        return [f"https://top.mail.ru/Rating/{keyword}/Today/Visitors/{p}.html"
                for p in range(1, self.pages + 1)]

    def scrap_websites(self, url):
        sleep(self.cooldown + random.random() * self.random_cooldown)
        return self.scrap_page(
            url,
            (self.website_template,),
        )

    def on_captcha_exception(self):
        self.logger.error("Sorry, we need to make sure that you are not a robot")
        sleep(self.cooldown + random.random() * self.random_cooldown)

        driver = Driver()
        driver.change_proxy()
        driver.change_useragent()
        driver.restart_session()
        driver.clear_cookies()

    def on_webdriver_exception(self):
        self.logger.error("Webdriver exception, potentially net error")
        sleep(self.cooldown + random.random() * self.random_cooldown)

        driver = Driver()
        driver.change_proxy()
        driver.restart_session()

    def captcha(self, markup):
        if self.captcha_catch.search(markup):
            return True
        return False

    @classmethod
    def website_template(cls, soup):
        return [item.select_one("a.t90.t_grey").get('href')
                for item in set([item.parent for item in soup.select("td.it-title > a.t90.t_grey")])]
