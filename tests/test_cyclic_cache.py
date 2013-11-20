from nose.tools import eq_, ok_

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
        eq_(list(iter(c)),range(n,i+n+1)+range(i+1,n))

def test_cyclic_cache_count():
    """
    Test that CyclicCache items count is good.
    """
    for cache_size in xrange(3,7):
        check_cyclic_cache_count(CyclicCache(cache_size),cache_size)

def test_cyclic_cache_values():
    """
    Test that CyclicCache values are good.
    """
    for cache_size in xrange(3,7):
        check_cyclic_cache_values(CyclicCache(cache_size),cache_size)

def test_cyclic_cache_factory():
    """
    Test that the CyclicCacheFactory returns good CyclicCache-s.
    """
    for cache_size in xrange(3,7):
        cf = CyclicCacheFactory(cache_size)
        check_cyclic_cache_values(cf(),cache_size)
        check_cyclic_cache_count(cf(),cache_size)
