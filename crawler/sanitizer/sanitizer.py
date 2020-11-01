from multiprocessing import Pool, cpu_count

from html_sanitizer import Sanitizer

from config import sanitizer_settings


def clean_webpage(file: tuple):

    with open(file[0], "r", encoding="utf-8") as input_f:
        html = input_f.read()
        input_f.close()

        with open(file[1], "w", encoding="utf-8") as output_f:
            sanitizer = Sanitizer(sanitizer_settings)
            output_f.write(sanitizer.sanitize(html))
            output_f.close()


def clean(pipe_data: dict):

    plain_docs = list(zip(pipe_data["raw_markup"], pipe_data["clean_markup"]))

    with Pool(cpu_count()) as pool:
        pool.map(clean_webpage, plain_docs)
        pool.close()
        pool.join()

    return pipe_data
