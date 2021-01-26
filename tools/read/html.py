from tools.fsys import files
from tools.text import remove_br, remove_strong, remove_li, remove_ul


def read_segments_in_html(path):
    preprocess = [
        remove_br,
        remove_li,
        remove_ul,
        remove_strong,
    ]

    fs = files(path, r".*\.html")

    content = []
    for file in fs:
        with open(file, "r") as f:
            res = " ".join(f.readlines())
            for p in preprocess:
                res = p(res)
            content.append(res)
    return content
