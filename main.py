import logging
import os
import signal
import sys
from logging.handlers import QueueHandler
from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing import cpu_count, Pool

import active_modules
import config
from crawler.web.driver import Driver
from initialization import filesys

log_format = "%(asctime)s - [%(name)s] %(levelname)s: %(message)s"
date_format = "%H:%M:%S"


def worker_initializer(queue):
    h = logging.handlers.QueueHandler(queue)
    root = logging.getLogger()
    root.addHandler(h)
    root.setLevel(logging.INFO)


def worker_termination(*args, **kwargs):
    logging.getLogger(f"pid={os.getpid()}").info("Terminating worker")
    Driver.close()
    sys.exit(0)


def logger_initializer(queue):
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
    filesys.init(config.paths)
    Driver.check_installation(config.webdriver_settings)

    signal.signal(signal.SIGTERM, worker_termination)
    default_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)

    proc_count = cpu_count()
    if config.sub_proc_count >= 1:
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
    logger.info(f"Using thread count: {proc_count}")

    signal.signal(signal.SIGINT, default_handler)

    Driver.check_installation(config.webdriver_settings)

    try:
        for m in active_modules.modules:
            m.do_job(p)

        p.map(Driver.close, range(proc_count), chunksize=1)

    except KeyboardInterrupt:
        logger.info(f"Keyboard interruption")
        p.terminate()

    p.close()
    p.join()

    q.put_nowait(None)
    logger_process.join()


if __name__ == "__main__":
    main()
