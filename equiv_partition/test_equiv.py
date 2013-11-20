from nose.tools import eq_, ok_
from equiv import CanonicalSet, EquivPart
from cyclic_cache import CyclicCache, CyclicCacheFactory

def check_cyclic_cache_count(c,n):
    """
    Test that c performes well as a CyclicCache with cache_size=n,
    from items count point-of-view.
    """
    for i in xrange(n):
        c.add(None)
        eq_(len(list(iter(c))),i+1)
    for i in xrange(n):
        c.add(None)
        eq_(len(list(iter(c))),n)

def check_cyclic_cache_values(c,n):
    """
    Test that c performes well as a CyclicCache with cache_size=n,
    from values point-of-view.
    """
    for i in xrange(n):
        c.add(i)
        eq_(list(iter(c)),range(i+1))
    for i in xrange(n):
        c.add(i+n)
        eq_(list(iter(c)),range(n,i+n+1)+range(i+1,4))

def test_cyclic_cache_count():
    """
    Test that CyclicCache items count is good.
    """
    check_cyclic_cache_count(CyclicCache(4),4)

def test_cyclic_cache_values():
    """
    Test that CyclicCache values are good.
    """
    check_cyclic_cache_values(CyclicCache(4),4)

def test_cyclic_cache_factory():
    """
    Test that the CyclicCacheFactory returns good CyclicCache-s.
    """
    cf = CyclicCacheFactory(4)
    check_cyclic_cache_values(cf(),4)
    check_cyclic_cache_count(cf(),4)
