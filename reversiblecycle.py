# -*- coding: utf-8 -*-


class ReversibleCycle:
    """Allow cyclic, reversible iteration through an indexable sequence.

    Notes:
        ReversibleCycle cycles like itertools.cycle.  However, it only
        works with indexable sequences (e.g. lists) and not, say, a zip.

    Args:
        seq: sequence to cycle through
    """

    def __init__(self, seq):
        self._seq = seq
        self._index = 0
        self._step = 1


    def reverse(self):
        """Switch the direction of iteration."""
        self._step = -1*self._step
        self._index = len(self._seq)-self._index+1


    def __iter__(self):
        return self


    def __next__(self):
        try:
            return self._seq[self._index]
        except IndexError:
            self._index = 0
            return self._seq[0]
        finally:
            self._index += self._step
