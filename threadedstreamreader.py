# -*- coding: utf-8 -*-

from threading import Thread
from queue import Queue


class ThreadedStreamReader(Thread):
    """Non-blocking stream reader based on threading.Thread.

    Credit to Eyal Arubas at https://gist.github.com/EyalAr/7915597
    
    Note:
        Calling the .is_alive() method tells whether this class is reading
        the stream. After the stream closes or before the thread starts,
        .is_alive() returns False.

    Args:
        stream: stream to read from
        *args, *kwargs: arguments to pass to Thread
    """

    def __init__(self, stream, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stream = stream
        self._queue = Queue()


    def run(self):
        while True:
            line = self._stream.readline()
            if not line:
                break
            self._queue.put(line)


    def read(self, timeout=None: float) -> str:
        """Get next line output by stream.

        Args:
            timeout (float): time to block for next line.
        """
        return self._queue.get(block=timeout is not None, timeout=timeout)

