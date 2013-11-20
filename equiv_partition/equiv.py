"""
Equivalence partitions.
"""
from cyclic_cache import CyclicCacheFactory
import hints

class EquivPart(object):
    """
    Maintains equivalence partitions for an unknown world.
    Assumes that sets are empty until otherwise convinced.
    For all assymptotical analysis, we denote the number of non-empty sets by n,
    and the number of disconnections performed by d. k is the cache-size - the
    number of sample elements stored for each set. We also assume that the
    number of possible results from each filter is bounded by r, and that
    these results are hashable.
    Storage is O(d+nk+n).
    """
    def __init__(self,cache_size=1):
        self._cache_factory = CyclicCacheFactory(cache_size)
        # This is a list of functions; order is important for indexing sets.
        self._filters = []
        # We start by assuming that the world is empty.
        # This is a dictionary from tuples of answers for filters, to a
        # canonical sets, which support: get_canonical, append_sample,
        # __div__ by a filter.
        self._sets = {}

    def enumerate(self):
        """
        This enumerates all sets that we are sure an non-empty. O(n).
        """
        return [x.get_canonical() for x in self._sets.values()]

    def disconnect(self,f,examples=None):
        """
        This disconnects all existing sets into two parts, according to the
        new filter. We attempt to see which sets actually split, to the best
        of our knowledge. O(n(k+r)).
        Examples is a list of examples for this filter, hopefully demonstrating 
        its capabilities with as much intersection as possible with other
        filters.
        """
        self._filters.append(f)
        new_sets = {}
        # We have many sets
        for index,set_ in self._sets.iteritems():
            subsets = set_ / f
            # We have at most r possible results.
            for value,new_set in subsets.items():
                new_sets[index + (value,)] = new_set
        self._sets = new_sets
        if examples is not None:
            for item in examples:
                self._inner_canonify(item,hints.EXAMPLE)

    def canonify(self,item):
        """
        Return the canonical item of the set given item belongs to.
        """
        s = self._inner_canonify(item,None)
        return s.get_canonical()

    def force_canon(self,item):
        """
        Force this item to become the canonical of its set.
        """
        s = self._get_set(item)
        if s is not None:
            s.force_canon(item,hints.FORCED_CANON)
        else:
            s = CanonicalSet(item,self._cache_factory,hints.FORCED_CANON)
            self._sets[index] = s
        return item

    def _get_set(self,item):
        """
        Return the set containing the given item, or None if doesn't exist yet.
        """
        index = tuple([f(item) for f in self._filters])
        if index in self._sets:
            return self._sets[index]
        else:
            return None

    def _inner_canonify(self,item,hint):
        """
        Return the canonical item for the set containing given item. O(d+k).
        Optionally accepts a hint, which will be passed on to cache to
        determine how strongly to hold on to this value.
        """
        s = self._get_set(item)
        if s is not None:
            s.append_sample(item,hint)
        else:
            s = CanonicalSet(item,self._cache_factory,hint)
            self._sets[index] = s
        return s
