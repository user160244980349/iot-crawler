import re


def template1(body):
    div = body.find("div", {"id": "detailBullets_feature_div"})
    if div is not None:
        for li in div.ul.findChildren("li"):
            spans = li.span.findChildren("span")
            text = re.sub(r"[\n\s]", "", spans[0].text)
            if re.match("^Manufacturer:$", text):
                return re.sub(r"[\"\',\n]", "", spans[1].text).lower()
    return None


def template2(body):
    div = body.find("table", {"id": "productDetails_detailBullets_sections1"})
    if div is not None:
        for tr in div.tbody.findChildren("tr"):
            text = re.sub(r"[\n\s]", "", tr.th.text)
            if re.search("^Manufacturer$", text):
                return re.sub(r"[\"\',\n]", "", tr.td.text).lower()
    return None


def template3(body):
    div = body.find("table", {"id": "productDetails_techSpec_section_1"})
    if div is not None:
        for tr in div.tbody.findChildren("tr"):
            text = re.sub(r"[\n\s]", "", tr.th.text)
            if re.search("^Manufacturer$", text):
                return re.sub(r"[\"\',\n]", "", tr.td.text).lower()
    return None


def product_template(soup):
    return [f"https://www.amazon.com{items.findChild('a').get('href')}"
            for items in soup.findAll("div", {"data-component-type": "s-search-result"})]
