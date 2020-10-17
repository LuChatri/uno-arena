# -*- coding: utf-8 -*-

import protocol
from threadedstreamreader import ThreadedStreamReader
from queue import Empty
from subprocess import Popen, PIPE
from time import sleep


class Engine:
    """An engine instance.

    Args:
        name: an identifier for the engine
        command (str): shell initialization command for engine

    """

    def __init__(self, name, command: str):
        self.name = name
        self._process = subprocess.Popen(args.command, shell=True,
                                        stdin=PIPE, stdout=PIPE, stderr=PIPE)
        self._reader = ThreadedStreamReader(self.process.stdout)
        self._reader.start()


    def is_alive(self) -> bool:
        """Check whether the engine process is running."""
        return self._process.poll() is None


    def stop(self, timeout=5: float):
        """Shut the engine down.

        Args:
            timeout (float): max time to block for safe shutdown
        """
        if self.is_alive()
            self.write(protocol.SHUTDOWN)
            # Give the engine time for a safe shutdown
            self.read(timeout=timeout)
            # Clean up the process forcefully
            self._process.kill()

        if self._reader.is_alive():
            self._reader.join()


    def write(self, msg):
        """Write a message to the engine."""
        if self.is_alive():
            self._process.write(msg)
            return True
        return False


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
                return self._reader.read(timeout)
            except Empty:
                return ''
        return False


    def ping(self, timeout=None):
        """Send a ping message and read the response."""
        self.write(protocol.PING)
        return self.read(timeout)


    def __del__(self):
        # Do cleanup
        self.finish()
        super().__del__()
