from nose.tools import eq_, ok_

from equiv import EquivPart

CACHE_SIZE = 4

class TestCanonicalSet(object):
    """
    Test CanonicalSet. Currently hints are unsupported.
    """
    def setup(self):
        self.ep = EquivPart(CACHE_SIZE)

    def test(self):
        eq_(self.ep.enumerate(),[])
        eq_(self.ep.canonify(0),0)
        eq_(self.ep.enumerate(),[0])
        eq_(self.ep.canonify(1),0)
        self.ep.disconnect(lambda x: x<0.5)
        eq_(set(self.ep.enumerate()),set([0,1]))
        eq_(self.ep.canonify(1),1)
        eq_(self.ep.canonify(2),1)
        eq_(self.ep.force_canon(2),2)
        eq_(self.ep.canonify(1),2)
        eq_(self.ep.canonify(0),0)
        eq_(self.ep.canonify(-1),0)
        def f1(x):
            if x < 0.5:
                return 0
            elif x > 0.5:
                return 1
            else:
                return 2
        self.ep.disconnect(f1)
        eq_(set(self.ep.enumerate()),set([0,2]))
        eq_(self.ep.canonify(1),2)
        eq_(self.ep.canonify(2),2)
        eq_(self.ep.canonify(0),0)
        eq_(self.ep.canonify(-1),0)
        eq_(self.ep.canonify(0.5),0.5)
        eq_(set(self.ep.enumerate()),set([0,0.5,2]))
