def objcount(cls):
    cls.counter = 0

    original_init = cls.__init__

    def new_init(self):
        cls.counter += 1
        original_init(self)

    cls.__init__ = new_init

    original_del = cls.__del__ if '__del__' in cls.__dict__ else None

    def new_del(self):
        cls.counter -= 1
        if original_del:
            original_del(self)

    cls.__del__ = new_del

    return cls

from sys import stdin
exec(stdin.read())
