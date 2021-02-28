import os

import config


def init():

    json = os.path.join(config.resources_abs, "json")
    op = os.path.abspath(config.original_policies)
    pp = os.path.abspath(config.processed_policies)
    plp = os.path.abspath(config.plain_policies)

    if not os.path.exists(config.resources_abs):
        os.makedirs(config.resources_abs)

    if not os.path.exists(json):
        os.makedirs(json)

    if not os.path.exists(op):
        os.makedirs(op)

    if not os.path.exists(pp):
        os.makedirs(pp)

    if not os.path.exists(plp):
        os.makedirs(plp)
