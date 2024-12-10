from collections import UserString


class DivStr(UserString):
    def __init__(self, init_str=""):
        super().__init__(init_str)

    def __floordiv__(self, n):
        length = len(self)
        if n <= 0:
            raise ValueError("Делитель должен быть положительным.")

        part_size = length // n

        parts = [self[i * part_size:(i + 1) * part_size]
                 for i in range(n)]

        return iter(parts)

    def __mod__(self, n):
        length = len(self)
        if n <= 0:
            raise ValueError("Делитель должен быть положительным.")

        remainder = length % n
        return self[-remainder:] if remainder else DivStr()

a = DivStr("89[0fupgiv;qwthwthwtt"*1000000)
print(a % 67408)

from sys import stdin
exec(stdin.read())


