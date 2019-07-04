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

def foreach(f,*seq):
    F.lmap(f,*seq)
    return None

if __name__ == '__main__':
    print( lmap(tup(pow))( [(2,5),(3,2),(10,3)] ) )
    print( list(starmap(pow)([(2,5),(3,2),(10,3)] ) ))
    print( lstarmap(pow)([(2,5),(3,2),(10,3)] ) )

    print( list(map(tup(pow))( [(2,5),(3,2),(10,3)] ) ))

    print(F.lmap(
        lambda a,b,c: a+b+c, [1,2,3],[2,3,4],[5,6,7]
    ))
