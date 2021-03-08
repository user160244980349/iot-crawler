import random
import re
from time import sleep

from crawler.plugins.plugin import Plugin


class Amazon(Plugin):
    sanitize_label = re.compile(r"[^\w]|[_]")
    sanitize_value = re.compile(r"[^\w ]|[_]")
    manufacturer = re.compile(r"^manufacturer$")
    captcha_catch = re.compile("sorry, we just need to make sure you're not a robot")

    def __init__(self, keywords, pages, cooldown=3., random_cooldown=3., sync=False):
        super().__init__(keywords, pages, sync)
        self.cooldown = cooldown
        self.random_cooldown = random_cooldown

    def gen_search_urls(self, keyword, pages):
        return [f"https://www.amazon.com/s?k={keyword}&page={p}"
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
            (self.template1, self.template2, self.template3),
        )

    def captcha(self, markup):
        if Amazon.captcha_catch.search(markup.lower()):
            return True
        return False

    @classmethod
    def product_template(cls, soup):
        return [f"https://www.amazon.com{items.findChild('a').get('href')}"
                for items in soup.findAll("div", {"data-component-type": "s-search-result"})]

    @classmethod
    def template1(cls, body):
        div = body.find("div", {"id": "detailBullets_feature_div"})
        if div is not None:
            for li in div.ul.findChildren("li"):
                spans = li.span.findChildren("span")
                if cls.manufacturer.match(cls.sanitize_label.sub("", spans[0].text.lower())):
                    return cls.sanitize_value.sub("", spans[1].text).lower()

    @classmethod
    def template2(cls, body):
        div = body.find("table", {"id": "productDetails_detailBullets_sections1"})
        if div is not None:
            for tr in div.tbody.findChildren("tr"):
                if cls.manufacturer.match(cls.sanitize_label.sub("", tr.th.text.lower())):
                    return cls.sanitize_value.sub("", tr.td.text).lower()

    @classmethod
    def template3(cls, body):
        div = body.find("table", {"id": "productDetails_techSpec_section_1"})
        if div is not None:
            for tr in div.tbody.findChildren("tr"):
                if cls.manufacturer.match(cls.sanitize_label.sub("", tr.th.text.lower())):
                    return cls.sanitize_value.sub("", tr.td.text).lower()
