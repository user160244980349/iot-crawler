import re
from multiprocessing import Pool


from crawler.plugins.amazon.routines import scrap_products, get_product
from crawler.plugins.plugin import Plugin
from tools.arrays import flatten_list


class Amazon(Plugin):

    def __init__(self, keywords, pages):
        super().__init__(keywords, pages)

    def gen_search_urls(self, keyword):
        return [f"https://www.amazon.com/s?k={keyword}&page={p}"
                for p in range(1, self.pages + 1)]

    def scrap(self, p: Pool):

        items = []

        for keyword in self.keywords:
            keyword_escaped = re.sub(r"\s", "+", keyword)
            search_urls = self.gen_search_urls(keyword_escaped)
            items_urls = p.map(scrap_products, search_urls)
            items_urls = flatten_list(items_urls)
            found_items = p.map(get_product, items_urls)

            for found_item in found_items:
                found_item["keyword"] = keyword

            items.extend(found_items)

        return items
