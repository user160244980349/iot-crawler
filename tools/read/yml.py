import yaml

from tools.fsys import files


def read_segments_in_yaml(path):
    fs = files(path, r".*\.yml")

    content = []
    for file in fs:
        with open(file, "r") as f:
            data = yaml.load(f, Loader=yaml.CLoader)
            for value in data["segments"]:
                content.append(value["segment_text"])
    return content
