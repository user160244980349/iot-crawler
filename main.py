import logging
import os
import signal
from logging.handlers import QueueHandler
from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing import cpu_count, Pool

from urllib3.exceptions import ProtocolError

import active_modules
import config
from crawler.web.driver import Driver
from initialization import filesys

log_format = "%(asctime)s - [%(name)s] %(levelname)s: %(message)s"
date_format = "%H:%M:%S"


def worker_initializer(queue):
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    h = logging.handlers.QueueHandler(queue)
    root = logging.getLogger()
    root.addHandler(h)
    root.setLevel(logging.INFO)


def local_initializer():
    logging.basicConfig(
        format=log_format,
        datefmt=date_format,
        level=logging.INFO
    )


def logger_initializer(queue):
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    f = logging.Formatter(log_format, date_format)
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
    filesys.init()

    proc_count = cpu_count()
    if config.sub_proc_count > 1 or config.sub_proc_count == 0:
        if config.sub_proc_count > 1:
            proc_count = config.sub_proc_count

        q = Queue(-1)
        logger_process = Process(target=logger_initializer,
                                 args=(q,))
        logger_process.start()

        p = Pool(proc_count,
                 initializer=worker_initializer,
                 initargs=(q,))

        worker_initializer(q)
        logger = logging.getLogger(f"pid={os.getpid()}")
        logger.info(f"Using thread count: {config.sub_proc_count}")

    else:
        p = None
        q = None
        logger_process = None
        local_initializer()
        logger = logging.getLogger(f"pid={os.getpid()}")

    try:
        for m in active_modules.modules:
            m.do_job(p)

    except ProtocolError:
        pass

    except Exception:
        import sys
        import traceback
        traceback.print_exc(file=sys.stderr)

    finally:

        if p is not None:
            logger.info(f"Closing process pool")

            p.map(Driver.close, (None for _ in range(proc_count)), chunksize=1)
            p.close()
            p.join()

            q.put_nowait(None)
            logger_process.join()

        Driver.close()


if __name__ == "__main__":
    main()
