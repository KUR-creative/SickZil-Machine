import utils.imutils as iu #TODO: make imutils minimal.
import utils.fp as fp
import cv2
from PyQt5.QtGui import QImage

load = fp.multi(lambda p,s=None: s)
NDARR = 'ndarr'
MASK  = 'mask' 
@fp.mmethod(load, None)
def load(path, type_str=None):
    return QImage(path)
@fp.mmethod(load, NDARR)
def load(path, type_str):
    return iu.imread(path)
@fp.mmethod(load, MASK)
def load(path, type_str):
    return iu.imread(path)

def save(path, img): #TODO: multimethod..?
    cv2.imwrite(path, img)

#def save(path, img, ndarr=False):

def load_qimg(path):
    return QImage(path)
    '''
    return fp.go(
        path,
        load,
        iu.channel3img,
        iu.nparr2qimg
    )
    '''

#def load_mask(path)
