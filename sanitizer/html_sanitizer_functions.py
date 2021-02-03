import re


def to_remove(element):
    element.tag = "to_remove"
    for c in element.getchildren():
        to_remove(c)
        element.remove(c)


def div_remover(element):
    s = list(element.classes)
    s.append(element.get('id'))
    s.append(element.tag)
    if re.match(r"^.*(head|foot|nav|bar|alert|modal|dialog|popup|banner|promo|side).*$",
                " ".join([i for i in s if i is not None]), flags=re.IGNORECASE) is not None:
        to_remove(element)
    return element


def div_to_p(element):
    if element.tag == "div":
        if len(element.getchildren()) == 0:
            element.tag = "p"

    return element


def remove_tags(soup, element):
    for e in soup.find_all(element):
        e.extract()
