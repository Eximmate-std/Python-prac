class Vowel:
    __slots__ = 'a', 'e', 'i', 'o', 'u', 'y'

    def __init__(self, a=None, e=None, i=None, o=None, u=None, y=None):
        self.a = a
        self.e = e
        self.i = i
        self.o = o
        self.u = u
        self.y = y


    def _check_full(self):
        return all(getattr(self, slot) is not None for slot in self.__slots__)

    def __str__(self):
        values = [f"{slot}: {getattr(self, slot)}" for slot in sorted(self.__slots__) if getattr(self, slot) is not None]
        return ', '.join(values)

    @property
    def answer(self):
        return 42

    @property
    def full(self):
        return self._check_full()

    @full.setter
    def full(self, value):
        pass

import sys
exec(sys.stdin.read())
