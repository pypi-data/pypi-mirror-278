from typing import Iterable, TypeVar

_T = TypeVar("_T")


class OrderedSet(set):
    def __init__(self, iterable=None):
        self._data = {}
        if iterable is not None:
            for item in iterable:
                self.add(item)

    def add(self, element: _T):
        self._data[element] = None

    def discard(self, element: _T):
        if element in self._data:
            del self._data[element]

    def __contains__(self, item):
        return item in self._data

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data.keys())

    def __repr__(self):
        return f"PartialSet({list(self._data.keys())})"

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return self._data == other._data
        return False

    def __ne__(self, value: object) -> bool:
        return not self == value

    def clear(self):
        self._data.clear()

    def pop(self):
        if not self._data:
            raise KeyError("pop from an empty OrderedSet")
        key = next(iter(self._data))
        self.discard(key)
        return key

    def update(self, s: Iterable[_T]) -> None:
        for item in s:
            self.add(item)

    def __getitem__(self, index):
        return list(self._data.keys())[index]

    def __reversed__(self):
        return reversed(list(self._data.keys()))

    def copy(self):
        return OrderedSet(self._data.keys())
