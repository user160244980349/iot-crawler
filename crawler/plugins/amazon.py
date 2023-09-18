import re

from crawler.plugins.plugin import Plugin


class Amazon(Plugin):
    sanitize_label = re.compile(r"[^\w]|_")
    sanitize_value = re.compile(r"[^\w ]|_")
    manufacturer = re.compile(r".*manufacturer.*", flags=re.IGNORECASE)

    def __init__(self, keywords, pages, products_json, cooldown=0.,
                 random_cooldown=0.):
        super().__init__(keywords, pages, products_json,
                         cooldown=cooldown, random_cooldown=random_cooldown)

    def gen_search_urls(self, keyword):
        return [f"https://www.amazon.com/s?k={keyword}&page={p}"
                for p in range(1, self.pages + 1)]

    def scrap_products(self, url):
        return self.scrap_page(
            url,
            (self.product_template,),
        )

    def get_product(self, url):
        return url, self.scrap_page(
            url,
            (self.template1, self.template2, self.template3),
        )

    def template1(self, body):
        try:
            div = body.find("div", {"id": "detailBullets_feature_div"})
            for li in div.ul.findChildren("li"):
                span = li.span.findChildren("span")
                label = self.sanitize_label.sub("", span[0].text)
                if self.manufacturer.match(label):
                    manufacturer = span[1].text
                    manufacturer = self.sanitize_value.sub(
                        "", manufacturer
                    ).lower()
                    self.logger.info(f"Got manufacturer {manufacturer}")
                    return manufacturer

        except (AttributeError, TypeError):
            self.logger.info("Template 1: Manufacturer field is not found")

    def template2(self, body):
        try:
            div = body.find("table",
                            {"id": "productDetails_detailBullets_sections1"})
            for tr in div.tbody.findChildren("tr"):
                span = tr.th.text
                span = self.sanitize_label.sub("", span)
                if self.manufacturer.match(span):
                    manufacturer = tr.td.text
                    manufacturer = self.sanitize_value.sub(
                        "", manufacturer
                    ).lower()
                    self.logger.info(f"Got manufacturer {manufacturer}")
                    return manufacturer

        except (AttributeError, TypeError):
            self.logger.error("Template 2: Manufacturer field is not found")

    def template3(self, body):
        try:
            div = body.find("table",
                            {"id": "productDetails_techSpec_section_1"})
            for tr in div.tbody.findChildren("tr"):
                span = tr.th.text
                span = self.sanitize_label.sub("", span)
                if self.manufacturer.match(span):
                    manufacturer = tr.td.text
                    manufacturer = self.sanitize_value.sub(
                        "", manufacturer
                    ).lower()
                    self.logger.info(f"Got manufacturer {manufacturer}")
                    return manufacturer

        except (AttributeError, TypeError):
            self.logger.error("Template 3: Manufacturer field is not found")

    @classmethod
    def product_template(cls, soup):
        return [f"https://www.amazon.com{items.findChild('a').get('href')}"
                for items in soup.findAll("div", {
                "data-component-type": "s-search-result"
            })]
