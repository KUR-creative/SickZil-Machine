import imageio
import utils.imutils as iu #TODO: make imutils minimal.
import utils.fp as fp
import numpy as np
import cv2
from PyQt5.QtGui import QImage

load = fp.multi(lambda p,s=None: s)
NDARR = 'ndarr'
IMAGE = 'image'
MASK  = 'mask' 

@fp.mmethod(load, None)
def load(path, type=None): return QImage(path)
@fp.mmethod(load, NDARR)
def load(path, type): return iu.imread(path)
@fp.mmethod(load, IMAGE)
def load(path, type): return iu.channel3img(iu.imread(path))
@fp.mmethod(load, MASK)
def load(path, type): return mask2segmap(iu.imread(path))

def segmap2mask(segmap):
    '''
    convert segmap(snet output) to mask(gui, file)

    segmap: np.uint8, bgr,  {fg=white, bg=black}
    mask:   np.uint8, bgra, {fg=red, bg=transparent}
    '''
    _,_,r = cv2.split(segmap) # b=g=r, a=r
    b = g = np.zeros_like(r)
    return cv2.merge((b,g,r,r))

def mask2segmap(mask):
    '''
    convert mask(gui, file) to segmap(snet output) 

    mask:   np.uint8, bgra, {fg=red, bg=transparent}
    segmap: np.uint8, bgr, b=g=r {fg=white, bg=black}
    '''
    return fp.go(
        mask,
        lambda m4: np.sum(m4[:,:,:3], axis=-1, dtype=np.uint8),
        lambda m1: np.expand_dims(m1, axis=-1),
        lambda m1: cv2.merge((m1,m1,m1))
    )

def save(path, img): #TODO: multimethod..?
    if len(img.shape) == 3:
        n_channels = img.shape[-1]
        if n_channels == 4:   # bgra -> rgba
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
        elif n_channels == 3: # bgr -> rgb
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    elif len(img.shape) == 2: # bw = bw
        rgb_img = img

    imageio.imwrite(path, rgb_img)
