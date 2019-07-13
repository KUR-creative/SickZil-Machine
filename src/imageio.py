import utils.imutils as iu #TODO: make imutils minimal.
import utils.fp as fp
import cv2
from PyQt5.QtGui import QImage

def load(path):
    # it can be cached..
    return iu.imread(path)

def save(path, img): #TODO: multimethod..?
    cv2.imwrite(path, img)

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
