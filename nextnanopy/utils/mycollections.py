from collections import OrderedDict


class DictList(OrderedDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def _idxs(self):
        return OrderedDict(enumerate(self.keys()))

    def __getitem__(self, key):
        if isinstance(key, int):
            key = self._idxs[key]
        item = super().__getitem__(key)
        return item

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        cname = self.__class__.__name__
        args = [f"(index: {idx} - key: '{key}' - {value})" for idx, key, value in
                zip(self._idxs.keys(), self.keys(), self.values())]
        args = ',\n'.join(args)
        return f"{cname}([\n{args}\n])"

    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        try:
            result = self.__getitem__(self._iter_index)
        except (IndexError, KeyError):
            raise StopIteration
        self._iter_index += 1
        return result
