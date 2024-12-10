class Num:
    def __init__(self):
        self.value = 0

    def __get__(self, instance, owner):
        return getattr(instance, "value", 0)

    def __set__(self, instance, value):
        if isinstance(value, (int, float)):
            instance.value = value
        elif hasattr(value, '__len__'):
            instance.value = len(value)

    def __add__(self, other):
        return self.value + other.value

import sys
exec(sys.stdin.read())