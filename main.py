import logging
from logging.handlers import QueueHandler
from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing import cpu_count, Pool

from config import sub_proc_count
from crawler.downloader import download
from crawler.web.driver import Driver
from sanitizer.sanitizer import clean


def worker_initializer(queue):
    h = logging.handlers.QueueHandler(queue)
    root = logging.getLogger()
    root.addHandler(h)
    root.setLevel(logging.DEBUG)


def logger_process(queue):
    f = logging.Formatter("%(asctime)s - [%(name)s] %(levelname)s: %(message)s", "%H:%M:%S")
    h = logging.StreamHandler()
    h.setLevel(logging.INFO)
    h.setFormatter(f)
    logging.getLogger().addHandler(h)

    while True:

        record = queue.get()

        if record is None:
            break

        logger = logging.getLogger(record.name)
        logger.handle(record)


def main():
    proc_count = cpu_count()
    if sub_proc_count > 0:
        proc_count = sub_proc_count

    q = Queue(-1)
    listener = Process(target=logger_process,
                       args=(q,))
    listener.daemon = True
    listener.start()

    worker_initializer(q)
    logger = logging.getLogger("Main process")
    logger.info(f"Using thread count: {proc_count}")

    p = Pool(proc_count,
             initializer=worker_initializer,
             initargs=(q,))

    try:
        # scrap_products(p)
        # websites(p)
        # policies(p)
        download(p)

        p.imap(Driver.close, [i for i in range(proc_count)])

        clean(p)

    except:
        import sys
        import traceback
        traceback.print_exc()
        exc_type, value = sys.exc_info()[:2]
        logger.error(f"{exc_type}\n"
                     f"{value}\n"
                     f"{traceback.format_exc()}")

    finally:
        logger.info(f"Closing process pool")

        p.imap(Driver.close, [i for i in range(proc_count)])

        p.close()
        p.join()

        q.put_nowait(None)
        listener.join()


if __name__ == '__main__':
    main()
