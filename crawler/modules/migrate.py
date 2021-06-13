from hashlib import md5
from multiprocessing import Pool

from mysql.connector import connect, Error
import os

from crawler.modules.module import Module


class Migrate(Module):

    def bootstrap(self):
        pass

    def finish(self):
        pass

    def run(self, p: Pool = None):

        try:

            path = os.path.abspath(os.path.join("./plain_policies"))
            fs = []
            for dir_path, dir_names, file_names in os.walk(path):
                fs.extend([os.path.join(dir_path, f) for f in file_names])

            names = []
            contents = []
            hashes = []

            for f in fs:
                with open(f, "r", encoding="utf-8") as fl:
                    c = fl.read()
                    names.append(os.path.basename(f))
                    contents.append(c)
                    hashes.append(md5(c.encode()).hexdigest())

            with connect(host="localhost",
                         user="iot_annotation",
                         password="secret") as connection:

                data = ", ".join(f"('{n}', '{c}', '{h}')" for n, c, h in list(zip(names, contents, hashes)))

                with connection.cursor() as cursor:
                    cursor.execute("USE iot_annotation;")
                    cursor.execute(f"INSERT INTO `texts` (`name`, `content`, `hash`) VALUES {data};")
                    connection.commit()

        except Error as e:
            print(e)
