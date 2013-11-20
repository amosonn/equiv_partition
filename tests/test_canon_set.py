from nose.tools import eq_, ok_

from canon_set import CanonicalSet
from cyclic_cache import CyclicCacheFactory

CACHE_SIZE = 4

class TestCanonicalSet(object):
    """
    Test CanonicalSet. Currently hints are unsupported.
    """
    @classmethod
    def setup_class(cls):
        cls.cf = CyclicCacheFactory(CACHE_SIZE)

    def setup(self):
        self.cs = CanonicalSet(0,self.cf)

    def test_get_canonical(self):
        """
        Test that get_canonical works.
        """
        eq_(self.cs.get_canonical(),0)

    def test_new_canon(self):
        """
        Test that new_canon changes canonical properly.
        """
        eq_(self.cs.get_canonical(),0)
        self.cs.new_canon(1)
        eq_(self.cs.get_canonical(),1)

    def test_clean_div(self):
        """
        Test that a div for a one-element set works.
        """
        div1 = self.cs / (lambda x: x == 0)
        eq_(len(div1),1)
        ok_(True in div1)
        eq_(div1[True].get_canonical(),0)
        div2 = self.cs / (lambda x: x)
        eq_(len(div2),1)
        ok_(0 in div2)
        eq_(div2[0].get_canonical(),0)

    def test_same_div(self):
        """
        Test that a div for a multi-element set, with all items in the same
        partition, works.
        """
        self.cs.append_sample(1)
        div1 = self.cs / (lambda x: x != 3)
        eq_(len(div1),1)
        ok_(True in div1)
        eq_(div1[True].get_canonical(),0)

    def test_different_div(self):
        """
        Test that a div for a multi-element set, with items in different
        partitions, works.
        """
        self.cs.append_sample(3)
        div1 = self.cs / (lambda x: x != 3)
        eq_(len(div1),2)
        ok_(True in div1)
        ok_(False in div1)
        eq_(div1[True].get_canonical(),0)
        eq_(div1[False].get_canonical(),3)
        self.cs.append_sample(1)
        div2 = self.cs / (lambda x: x)
        eq_(len(div2),3)
        for i in [0,1,3]:
            ok_(i in div2)
            eq_(div2[i].get_canonical(),i)
