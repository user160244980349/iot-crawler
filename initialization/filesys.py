import os

from config import resources, original_policies, processed_policies


def init():

    json = os.path.join(resources, "json")
    op = os.path.join(resources, original_policies)
    pp = os.path.join(resources, processed_policies)

    if not os.path.exists(resources):
        os.makedirs(resources)

    if not os.path.exists(json):
        os.makedirs(json)

    if not os.path.exists(op):
        os.makedirs(op)

    if not os.path.exists(pp):
        os.makedirs(pp)
