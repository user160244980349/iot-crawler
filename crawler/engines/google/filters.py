import re

from tools.text import similarity


def check_first(soup):
    cut = r"(^http://|^https://|www\.|/$)"
    url = soup.find("cite").text
    return f"https://{re.sub(cut, '', url)}"


def check_similarity(content, soup, threshold=.6):
    cut = r"(^https?://|^https?://|www\.|/$)"
    best_url = None
    best_similarity = threshold

    for c in soup.find_all("cite"):

        url_match = re.match(r"((^www\.|^)([\w\d.\-_]+)\.\w+).*$", c.text)

        content = re.sub(r"[.,:/\\]|\s+", " ", content)
        content_pieces = content.split()
        if len(content_pieces) > 1:
            content_pieces.append("".join(content_pieces))

        for piece in content_pieces:
            if url_match is not None:
                url = url_match.group(1)
                domain = url_match.group(3)
                sim = similarity(piece, domain)

                if sim > best_similarity:
                    best_url = url
                    best_similarity = sim

    if best_url is not None:
        return f"http://{re.sub(cut, '', best_url)}"
    return None
