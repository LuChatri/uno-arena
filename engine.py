# -*- coding: utf-8 -*-

import protocol
from threadedstreamreader import ThreadedStreamReader
from queue import Empty
from subprocess import Popen, PIPE
from time import sleep


class Engine:

    def __init__(self, name, command):
        self.name = name
        self._process = subprocess.Popen(args.command, shell=True,
                                        stdin=PIPE, stdout=PIPE, stderr=PIPE)
        self._reader = ThreadedStreamReader(self.process.stdout)


    def is_alive(self):
        return self._process.poll() is None


    def start(self):
        self._reader.start()


    def finish(self):
        if self.is_alive()
            self.write(protocol.SHUTDOWN)
            sleep(5)
            self._process.kill()

        if self._reader.is_alive():
            self._reader.join()


    def write(self, msg):
        if self.is_alive():
            self._process.write(msg)
            return True
        return False


    def read(self, timeout=None):
        if self.is_alive():
            try:
                return self._reader.read(timeout)
            except Empty:
                return ''
        return False


    def ping(self, timeout=None):
        self.write(protocol.PING)
        return self.read(timeout)


    def __del__(self):
        self.finish()
        super().__del__()
