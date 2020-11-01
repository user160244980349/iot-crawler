from os.path import join

from config import urls, original_policies, processed_policies
from crawler.downloader.tools import url_to_name


def resolve(pipe_data: dict):

    pipe_data["urls"] = urls
    file_names = [url_to_name(u) for u in urls]
    pipe_data["raw_markup"] = [join(original_policies, f) for f in file_names]
    pipe_data["clean_markup"] = [join(processed_policies, f) for f in file_names]

    return pipe_data
