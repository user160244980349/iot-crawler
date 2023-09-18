import json
import os


def init(paths):
    if not os.path.exists(paths.resources):
        os.makedirs(paths.resources)

        os.chdir(paths.resources)

        os.makedirs(os.path.join(paths.resources, "json"))

        os.makedirs(paths.dir.original)
        os.makedirs(paths.dir.processed)
        os.makedirs(paths.dir.plain)

        with open(os.path.relpath(paths.explicit), "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)

    else:
        os.chdir(paths.resources)
