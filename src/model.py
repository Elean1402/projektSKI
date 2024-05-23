
class TupleList(list):
    def append(self, item):
        if isinstance(item, tuple):
            super().append(item)
        else:
            raise TypeError("item is not tuple")