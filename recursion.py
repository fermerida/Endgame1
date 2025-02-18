import sys
import itertools

class RecursiveBlowup1:
    def __init__(self):
        self.__init__()

def test_init():
    return RecursiveBlowup1()

class RecursiveBlowup2:
    def __repr__(self):
        return repr(self)

def test_repr():
    return repr(RecursiveBlowup2())

class RecursiveBlowup4:
    def __add__(self, x):
        return x + self

def test_add():
    return RecursiveBlowup4() + RecursiveBlowup4()

class RecursiveBlowup5:
    def __getattr__(self, attr):
        return getattr(self, attr)

def test_getattr():
    return RecursiveBlowup5().attr

class RecursiveBlowup6:
    def __getitem__(self, item):
        return self[item - 2] + self[item - 1]

def test_getitem():
    return RecursiveBlowup6()[5]

def test_recurse():
    return test_recurse()

def test_cpickle(_cache={}):
    try:
        import cPickle
    except ImportError:
        print ("cannot import cPickle, skipped!")
        return
    l = None
    for n in itertools.count():
        try:
            l = _cache[n]
            continue  # Already tried and it works, let's save some time
        except KeyError:
            for i in range(100):
                l = [l]
        cPickle.dumps(l, protocol=-1)
        _cache[n] = l

def check_limit(n, test_func_name):
    sys.setrecursionlimit(n)
    if test_func_name.startswith("test_"):
        print (test_func_name[5:])
    else:
        print (test_func_name)
    test_func = globals()[test_func_name]
    try:
        test_func()
    # AttributeError can be raised because of the way e.g. PyDict_GetItem()
    # silences all exceptions and returns NULL, which is usually interpreted
    # as "missing attribute".
    except (RuntimeError, AttributeError):
        pass
    else:
        print ("Yikes!")

limit = 1000
while 1:
    check_limit(limit, "test_recurse")
    check_limit(limit, "test_add")
    check_limit(limit, "test_repr")
    check_limit(limit, "test_init")
    check_limit(limit, "test_getattr")
    check_limit(limit, "test_getitem")
    check_limit(limit, "test_cpickle")
    print ("Limit of %d is fine" % limit)
    limit = limit + 100