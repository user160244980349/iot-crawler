import re

from crawler.plugins.plugin import Plugin


class Walmart(Plugin):
    sanitize_label = re.compile(r"[^\w]|_")
    sanitize_value = re.compile(r"[^\w ]|_")
    manufacturer = re.compile(r"^manufacturer$", flags=re.IGNORECASE)
    brand = re.compile(r"^brand$", flags=re.IGNORECASE)
    captcha_catch = re.compile("verify your identity", flags=re.IGNORECASE)

    def __init__(self, keywords, pages, products_json, cooldown=0.,
                 random_cooldown=0.):

        super().__init__(keywords, pages, products_json, cooldown=cooldown,
                         random_cooldown=random_cooldown)

    def gen_search_urls(self, keyword):
        return [
            f"https://www.walmart.com/search/?page={p}&ps=40&query={keyword}"
            for p in range(1, self.pages + 1)]

    def scrap_products(self, url):
        return self.scrap_page(
            url,
            (self.product_template,),
        )

    def get_product(self, url):
        return url, self.scrap_page(
            url,
            (self.template1, self.template2),
        )

    @classmethod
    def product_template(cls, soup):
        return [f"https://www.walmart.com{item.get('href')}"
                for item in soup.findAll("a", {"class": "product-title-link"})]

    def template1(self, body):
        try:
            div = body.find("table", {"class": "product-specification-table"})
            for tr in div.tbody.findChildren("tr"):
                tds = tr.findChildren("td")
                label = self.sanitize_label.sub("", tds[0].text)
                if self.manufacturer.search(label):
                    manufacturer = tds[1].text
                    self.logger.info(f"Got manufacturer {manufacturer}")
                    return self.sanitize_value.sub("", manufacturer).lower()

        except (AttributeError, TypeError):
            self.logger.error("Template 1: Manufacturer field is not found")

    def template2(self, body):
        try:
            div = body.find("table", {"class": "product-specification-table"})
            for tr in div.tbody.findChildren("tr"):
                tds = tr.findChildren("td")
                label = self.sanitize_label.sub("", tds[0].text)
                if self.brand.search(label):
                    manufacturer = tds[1].text
                    self.logger.info(f"Got manufacturer {manufacturer}")
                    return self.sanitize_value.sub("", manufacturer).lower()

        except (AttributeError, TypeError):
            self.logger.error("Template 2: Manufacturer field is not found")
