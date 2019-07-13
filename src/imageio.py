import utils.imutils as iu #TODO: make imutils minimal.
import utils.fp as fp

def load(path):
    # it can be cached..
    return fp.go( 
        path,
        iu.imread,
        iu.channel3img,
        iu.nparr2qimg,
    )
