import logging
import os
import re
from time import sleep

from crawler.plugins.plugin import Plugin


class Amazon(Plugin):

    def __init__(self, keywords, pages, cooldown=3.):
        super().__init__(keywords, pages)
        self.cooldown = cooldown

    def gen_search_urls(self, keyword, pages):
        return [f"https://www.amazon.com/s?k={keyword}&page={p}"
                for p in range(1, pages + 1)]

    def scrap_products(self, url):
        sleep(self.cooldown)
        return self.scrap_products_base(url, self.product_template)

    def get_product(self, product):
        sleep(self.cooldown)
        return self.get_product_base(
            product,
            (self.template1, self.template2, self.template3),
            captcha=self.captcha
        )

    @classmethod
    def captcha(cls, markup):
        logger = logging.getLogger(f"pid={os.getpid()}")
        if re.search("Sorry, we just need to make sure you're not a robot.", markup):
            logger.error("Sorry, we just need to make sure you're not a robot.")
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
                text = re.sub(r"[\n\s]", "", spans[0].text)
                if re.match("^Manufacturer:$", text):
                    return re.sub(r"[\"\',\n]", "", spans[1].text).lower()
        return None

    @classmethod
    def template2(cls, body):
        div = body.find("table", {"id": "productDetails_detailBullets_sections1"})
        if div is not None:
            for tr in div.tbody.findChildren("tr"):
                text = re.sub(r"[\n\s]", "", tr.th.text)
                if re.search("^Manufacturer$", text):
                    return re.sub(r"[\"\',\n]", "", tr.td.text).lower()
        return None

    @classmethod
    def template3(cls, body):
        div = body.find("table", {"id": "productDetails_techSpec_section_1"})
        if div is not None:
            for tr in div.tbody.findChildren("tr"):
                text = re.sub(r"[\n\s]", "", tr.th.text)
                if re.search("^Manufacturer$", text):
                    return re.sub(r"[\"\',\n]", "", tr.td.text).lower()
        return None
