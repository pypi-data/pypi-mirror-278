import collections
import itertools
import operator


class GroupByAttr:
    def __init__(self, attr_name, grouping_map, default_group="others"):
        self._attr_name = attr_name
        self._default_group = default_group
        self._grouping = dict(map(reversed, grouping_map.items()))
        self._key_func = operator.attrgetter(self._attr_name)

    def __call__(self, iterable):
        iterable = sorted(iterable, key=self._key_func)
        grouped = itertools.groupby(iterable, key=self._key_func)

        result = collections.defaultdict(list)
        for key_value, it in grouped:
            key = self._grouping.get(key_value, self._default_group)
            result[key].extend(it)

        return result
