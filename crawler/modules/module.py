from multiprocessing import Pool


class Module:

    def __init__(self, sync=False):
        self.records = []
        self.sync = sync

    def do_job(self, p: Pool = None):
        self.bootstrap()

        if self.sync:
            self.run()
        else:
            self.run(p)

        self.finish()

    def bootstrap(self):
        raise NotImplementedError("Module is not implemented!")

    def finish(self):
        raise NotImplementedError("Module is not implemented!")

    def run(self, p: Pool = None):
        raise NotImplementedError("Module is not implemented!")
