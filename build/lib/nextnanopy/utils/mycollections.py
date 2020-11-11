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

    def __str__(self):
        out = super().__str__()
        args = [f"({idx},'{key}',{value})" for idx, key, value in zip(self._idxs.keys(), self.keys(), self.values())]
        args = ',\n'.join(args)
        return f"{out.split('[')[0]}[\n{args}\n]{out.split(']')[-1]}"
