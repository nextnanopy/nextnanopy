from collections import OrderedDict


class DictList(OrderedDict):
    """
        This is a customized collections.OrderedDict
        It is a mixture between a dictionary and a list because it allows to
        access the values via keys or integer indexes.
        Common usage:
            d = DictList(a=3, b='t')
            d[0] = 3
            d['a'] = 3

        It has all the methods and attributes from a dictionary like .keys(), .values(), .items()

        Moreover, it supports iterations like a list:
        for value in d:
            print(value)
        >>> 3
        >>> 't'


    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def _idxs(self):
        return OrderedDict(enumerate(self.keys()))

    def get_indx(self, key):
        for i, _key in enumerate(self.keys()):
            if _key == key:
                return i
        raise KeyError('No such key in the DictList')

    def __getitem__(self, key):
        if isinstance(key, int):
            if key < 0:
                key = len(self) + key
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
