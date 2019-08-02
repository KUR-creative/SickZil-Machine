import funcy as F
import itertools as I

tup = lambda f: lambda argtup: f(*argtup)
go = lambda x,*fs: F.rcompose(*fs)(x)
pipe = F.rcompose

def map(f,*seq):
    return F.map(f,*seq) if seq \
    else lambda *xs: F.map(f,*xs)
def lmap(f,*seq):
    return F.lmap(f,*seq) if seq \
    else lambda *xs: F.lmap(f,*xs)

def starmap(f,*seq):
    return I.starmap(f,*seq) if seq \
    else lambda *xs: I.starmap(f,*xs)
def lstarmap(f,*seq):
    return list(I.starmap(f,*seq)) if seq \
    else lambda *xs: list(I.starmap(f,*xs))

def filter(f,*seq):
    return F.filter(f,*seq) if seq \
    else lambda *xs: F.filter(f,*xs)
def lfilter(f,*seq):
    return F.lfilter(f,*seq) if seq \
    else lambda *xs: F.lfilter(f,*xs)

def remove(f,*seq):
    return F.remove(f,*seq) if seq \
    else lambda *xs: F.remove(f,*xs)
def lremove(f,*seq):
    return F.lremove(f,*seq) if seq \
    else lambda *xs: F.lremove(f,*xs)

def foreach(f,*seq):
    F.lmap(f,*seq)
    return None

def is_empty(coll):
    if coll:
        return False
    else:
        return True

# http://codeblog.dhananjaynene.com/2010/08/clojure-style-multi-methods-in-python/
def multi(switcher_func):
    """ Declares a multi map based method which will switch to the
    appropriate function based on the results of the switcher func"""
    def dispatcher(*args, **kwargs):
        key = switcher_func(*args, **kwargs)
        func = dispatcher.dispatch_map[key]
        if func :
            return func(*args,**kwargs)
        else :
            raise Exception("No function defined for dispatch key: %s" % key)
    dispatcher.dispatch_map = {}
    return dispatcher

def mmethod(dispatcher, result):
    """ The multi method decorator which allows one method at a time
    to be added to the broader switch for the given result value"""
    def inner(wrapped):
        dispatcher.dispatch_map[result] = wrapped
        # Change the method name from clashing with the multi and allowing
        # all multi methods to be written using the same name
        wrapped.__name__ = "_" + wrapped.__name__ + "_" + str(result)
        return dispatcher
    return inner


if __name__ == '__main__':
    def matcher(x,y=None):
        return y
    test = multi(matcher)

    @mmethod(test, None)
    def test(x,y=None): return x + str(y) + ' = None'
    @mmethod(test, '2')
    def test(x,y): return x + y + ' 2 str'
    @mmethod(test, '3')
    def test(x,y): return x + y + ' 3 str'

    print( lmap(tup(pow))( [(2,5),(3,2),(10,3)] ) )
    print( list(starmap(pow)([(2,5),(3,2),(10,3)] ) ))
    print( lstarmap(pow)([(2,5),(3,2),(10,3)] ) )

    print( list(map(tup(pow))( [(2,5),(3,2),(10,3)] ) ))

    print(F.lmap(
        lambda a,b,c: a+b+c, [1,2,3],[2,3,4],[5,6,7]
    ))
    print(test('1',None))
    print(test('1'))
    print(test('2','2'))
    print(test('2','3'))
