import random
import re
from time import sleep

from crawler.plugins.plugin import Plugin


class Walmart(Plugin):
    sanitize_label = re.compile(r"[^\w]|[_]")
    sanitize_value = re.compile(r"[^\w ]|[_]")
    manufacturer = re.compile(r"^manufacturer$")
    brand = re.compile(r"^brand$")
    captcha_catch = re.compile("verify your identity")

    def __init__(self, keywords, pages, cooldown=3., random_cooldown=3., sync=False):
        super().__init__(keywords, pages, sync)
        self.cooldown = cooldown
        self.random_cooldown = random_cooldown

    def gen_search_urls(self, keyword, pages):
        return [f"https://www.walmart.com/search/?page={p}&query={keyword}"
                for p in range(1, pages + 1)]

    def scrap_products(self, url):
        sleep(self.cooldown + random.random() * self.random_cooldown)
        return self.scrap_products_base(
            url,
            self.product_template,
        )

    def get_product(self, product):
        sleep(self.cooldown + random.random() * self.random_cooldown)
        return self.get_product_base(
            product,
            (self.template1, self.template2),
        )

    def captcha(self, markup):
        if Walmart.captcha_catch.search(markup.lower()):
            return True
        return False

    @classmethod
    def product_template(cls, soup):
        return [f"https://www.walmart.com{item.get('href')}"
                for item in soup.findAll("a", {"class": "product-title-link"})]

    @classmethod
    def template1(cls, body):
        div = body.find("table", {"class": "product-specification-table"})
        if div is not None:
            for tr in div.tbody.findChildren("tr"):
                tds = tr.findChildren("td")
                if cls.manufacturer.search(cls.sanitize_label.sub("", tds[0].text.lower())):
                    return cls.sanitize_value.sub("", tds[1].text).lower()

    @classmethod
    def template2(cls, body):
        div = body.find("table", {"class": "product-specification-table"})
        if div is not None:
            for tr in div.tbody.findChildren("tr"):
                tds = tr.findChildren("td")
                if cls.brand.search(cls.sanitize_label.sub("", tds[0].text.lower())):
                    return cls.sanitize_value.sub("", tds[1].text).lower()
