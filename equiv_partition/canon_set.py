"""
Canonical set.
"""

class CanonicalSet(object):
    """
    A representation of a small sample from a set, including a canonical item.
    Gets the cache_holder to use, and possibly more kwargs to pass to it.
    For all assymptotical analysis, we denote the cache-size by k.
    """
    def __init__(self,canonical,cache_factory,canon_hint=None):
        self._canonical = canonical
        self._cache = cache_factory()
        self._cache_factory = cache_factory
        self._canon_hint = canon_hint

    def get_canonical(self):
        """
        Get the canonical item of this set. O(1)
        """
        return self._canonical

    def append_sample(self,item,hint=None):
        """
        Append a sample item to this set. O(1)
        """
        self._cache.add(item,hint)

    def new_canon(self,canon,canon_hint=None):
        """
        Replace the canonical representation for this set.
        """
        self.append_sample(self._canonical,self._canon_hint)
        self._canonical = canon
        self._canon_hint = canon_hint

    def __div__(self,f):
        """
        Split self into CanonicalSet-s, according to the values of filter f.
        Returns a dict for received values and corresponding CanonicalSet.
        O(k)
        """
        d = {f(self._canonical) : CanonicalSet(self._canonical, \
            self._cache_factory)}
        for item in self._cache:
            val = f(item)
            if val in d:
                d[val].append_sample(item)
            else:
                d[val] = CanonicalSet(item,self._cache_factory)
        return d
