"""
Simple cache implementation.
"""

class CyclicCacheFactory(object):
    """
    A factory for CyclicCache-s of given cache size.
    """
    def __init__(self,cache_size):
        self._cache_size = cache_size

    def __call__(self):
        return CyclicCache(self._cache_size)

class CyclicCache(object):
    """
    A cached unordered set for a limited amount of objects. No assumptions
    about them.
    """
    def __init__(self,cache_size):
        self._cache_size = cache_size
        # List of cached items.
        # NOTE: this is maintained as a list, because we want to work with
        # non-hashables as well.
        self._items = []
        # Index of oldest item.
        self._next_other = 0

    def add(self,item,hint=None):
        """
        Add a new item to the cache, possibly replacing an old one.
        """
        if len(self._items) == self._cache_size:
            self._items[self._next_other] = item
        else:
            self._items.append(item)
        self._next_other += 1
        self._next_other %= self._cache_size

    def __iter__(self):
        """
        Iterate over all items still in the cache.
        """
        for i in self._items:
            yield i
