# -*- coding: utf-8 -*-

import protocol
from threadedstreamreader import ThreadedStreamReader
from queue import Empty
from subprocess import Popen, PIPE
from time import time


class Engine:
    """An engine instance.

    Attrs:
        name: an identifier for the engine

    Args:
        name: an identifier for the engine
        command (str): shell initialization command for engine
    """

    def __init__(self, name, command: str):
        self.name = name
        self.command = command
        self._process = subprocess.Popen(self.command,
                                         shell=True,
                                         stdin=PIPE,
                                         stdout=PIPE,
                                         stderr=PIPE)
        self._reader = ThreadedStreamReader(self.process.stdout)
        self._reader.start()


    def is_alive(self) -> bool:
        """Check whether the engine process is running."""
        return self._process.poll() is None


    def stop(self):
        """Shut the engine down nicely."""
        if self.is_alive():
            self._process.write(protocol.SHUTDOWN)
            t = time()
            
            while True:
                elapsed = time() - t
                timeout = protocol.SHUTDOWN_TIMEOUT - elapsed
                if timeout < 0:
                    self.force_stop()
                    break

                msg = self._reader(timeout)

                if msg is False:
                    self.force_stop()
                    break
                
                if msg[0] == protocol.SHUTTINGDOWN:
                    self.force_stop()
                    break
                elif msg[0] == protocol.ERROR:
                    self.force_stop()
                    print(msg)
                    break


    def force_stop(self):
        """Forcibly shut the engine down."""
        if not self.is_alive()
            self._process.kill()

        if self._reader.is_alive():
            self._reader.join()


    def read(self, timeout=None: float):
        """Read a message from the engine.

        Note:
            Returns False if the engine's output stream cannot be read.
            Returns '' if the output stream can be read, but there is nothing
            to read.

        Args:
            timeout (float): max time to block for reading
        """
        if self.is_alive():
            try:
                msg = self._reader.read(timeout).strip()
                return msg.lower.split()
            except Empty:
                return ''
        return False


    def write(self, msg):
        """Write a message to the engine."""
        if self.is_alive():
            self._process.write(msg + '\n')


    def __del__(self):
        # Do cleanup
        self.force_stop()
        super().__del__()
