import re
from os import walk
from os.path import join, isfile, abspath

from config import resources


def files(path: str, pattern: str):
    path = abspath(join(resources, path))
    fs = []
    for (dir_path, dir_names, file_names) in walk(path):
        fs.extend([join(dir_path, f) for f in file_names if re.match(pattern, f) is not None])
    return fs


def is_locked(path):
    if isfile(join(resources, path)):
        return True
    else:
        return False


def lock(path):
    f = open(path, 'w')
    f.close()
