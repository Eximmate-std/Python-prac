from collections import defaultdict

class Omnibus:
    _attributes_count = defaultdict(set)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
            return
        self._attributes_count[name].add(self)

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        return len(self._attributes_count[name])

    def __delattr__(self, name):
        if name.startswith("_"):
            super().__delattr__(name)
            return
        if self in self._attributes_count[name]:
            self._attributes_count[name].remove(self)


from sys import stdin
exec(stdin.read())