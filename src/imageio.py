import utils.imutils as iu #TODO: make imutils minimal.
import utils.fp as fp

def load(path):
    # it can be cached..
    return iu.imread(path)

def load_qimg(path):
    return iu.nparr2qimg(load(path))
