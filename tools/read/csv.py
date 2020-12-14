import csv
from os.path import join

from config import resources


def csv_write(rows: list, file: str):
    with open(join(resources, file), "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
        f.close()


def csv_read(file: str):
    with open(join(resources, file), "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        lines = [line for line in reader]
        f.close()
        return lines
