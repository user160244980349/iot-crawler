import os

from config import resources_abs, original_policies, processed_policies


def init():

    json = os.path.join(resources_abs, "json")
    op = os.path.abspath(original_policies)
    pp = os.path.abspath(processed_policies)

    if not os.path.exists(resources_abs):
        os.makedirs(resources_abs)

    if not os.path.exists(json):
        os.makedirs(json)

    if not os.path.exists(op):
        os.makedirs(op)

    if not os.path.exists(pp):
        os.makedirs(pp)
