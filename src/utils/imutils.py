import os
from PyQt5.QtGui import QImage
import cv2
import numpy as np
import imghdr

#---------------------------------------------------------------------------------
def is_img_file(fpath):
    return(not(imread(fpath) is None) 
        if os.path.isfile(fpath)
      else False)

def unique_colors(img):
    ''' 
    Get unique color of image in [[r,g,b] ..]. 
    It's very slow! it just for debugging.
    '''
    return np.unique(img.reshape(-1,img.shape[2]), axis=0)

def float32(uint8img):
    ''' Convert uint8img(0~255) image to float32(0. ~ 1.) image '''
    c = 1 if len(uint8img.shape) == 2 else 3
    h,w = uint8img.shape[:2]
    float32img = (uint8img / 255).astype(np.float32)
    #print('channel:',c)
    return float32img.reshape((h,w,c))

def uint8(img0_1): # img color range: [0.0 ~ 1.0]
    ''' Convert float32(0. ~ 1.) image to  uint8img(0~255) image '''
    return (img0_1 * 255).astype(np.uint8)

def binarization(img, threshold=100):
    binarized = (img >= threshold).astype(np.uint8) * 255
    return binarized

def modulo_padded(img, modulo=16):
    ''' Pad 0 pixels to image to make modulo * x width/height '''
    h,w = img.shape[:2]
    h_padding = (modulo - (h % modulo)) % modulo
    w_padding = (modulo - (w % modulo)) % modulo
    if len(img.shape) == 3:
        return np.pad(img, [(0,h_padding),(0,w_padding),(0,0)], mode='reflect')
    elif len(img.shape) == 2:
        return np.pad(img, [(0,h_padding),(0,w_padding)], mode='reflect')

#---------------------------------------------------------------------------------
def imread(fpath):
    '''
    `fpath` could be windows path (even includes unicode!) 
    (cv2.imread cannot work with unicode and windows path)
    If no file or can't decode with cv2.imdecode, then return None.

    Assert that fpath is not directory.
    If data of fpath is invalid image(or not an image), then return None
    '''
    with open(fpath,'rb') as stream: 
        bytes = bytearray(stream.read())
        nparr = np.asarray(bytes, dtype=np.uint8)
        if len(nparr):
            return cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

def nparr2qimg(cvimg):
    ''' convert cv2 bgr image -> rgb qimg '''
    h,w,c = cvimg.shape
    byte_per_line = w * c #cvimg.step() #* step # NOTE:when image format problem..
    return QImage(cvimg.data, w,h, byte_per_line, 
                  QImage.Format_RGB888).rgbSwapped()

def np_bgra2qimg(cvimg):
    ''' convert cv2 bgr image -> rgb qimg '''
    h,w,c = cvimg.shape
    byte_per_line = w * c #cvimg.step() #* step # NOTE:when image format problem..
    return QImage(cvimg.data, w,h, byte_per_line, 
                  QImage.Format_RGBA8888).rgbSwapped()

def qimg2nparr(qimg): 
    ''' convert rgb qimg -> cv2 bgr image '''
    #NOTE: it would be changed or extended to input image shape 
    # Now it just used for canvas stroke.. but in the future... I don't know :(

    #qimg = qimg.convertToFormat(QImage.Format_RGB32)
    #qimg = qimg.convertToFormat(QImage.Format_RGB888)
    h,w = qimg.height(), qimg.width()
    ptr = qimg.constBits()
    ptr.setsize(h * w * 4)
    print(h,w,ptr)
    return np.frombuffer(ptr, np.uint8).reshape(h, w, 4)  #  Copies the data
    #return np.array(ptr).reshape(h, w, 3)  #  Copies the data

def channel3img(img):
    '''
    If img is 3-channel img(h,w,3) then this is identity funcion.
    If img is grayscale img(h,w) then convert 3-channel img.
    If img is bgra img, then CONVERT to bgr(TODO: warning required!)
    else return None
    '''
    if len(img.shape) == 2:   # if grayscale image, convert.
        return cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    elif len(img.shape) == 3: 
        _,_,c = img.shape
        if c == 3: # BGR(RGB)
            return img
        elif c == 4: # BGRA(RGBA)
            return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR) 
            #NOTE: warning: no alpha!
    #else: None

#---------------------------------------------------------------------------------
# for segmap
rgb2wk_map = {
    (0., 1.) : [1.0, 1.0, 1.0],
    (1., 0.) : [0.0, 0.0, 0.0]
}

def map_max_row(img, val=1):
    ''' [max, a, b] -> [1, 0, 0] (custom round function) '''
    assert len(img.shape) == 3
    img2d = img.reshape(-1,img.shape[2])
    ret = np.zeros_like(img2d)
    ret[np.arange(len(img2d)), img2d.argmax(1)] = val
    return ret.reshape(img.shape)

# https://github.com/keras-team/keras/blob/master/keras/utils/np_utils.py
def to_categorical(y, num_classes=None, dtype='float32'):
    """
    Converts a class vector (integers) to binary class matrix.
    E.g. for use with categorical_crossentropy.
    # Arguments
        y: class vector to be converted into a matrix
            (integers from 0 to num_classes).
        num_classes: total number of classes.
        dtype: The data type expected by the input, as a string
            (`float32`, `float64`, `int32`...)
    # Returns
        A binary matrix representation of the input. The classes axis
        is placed last.
    # Example
    ```python
    # Consider an array of 5 labels out of a set of 3 classes {0, 1, 2}:
    > labels
    array([0, 2, 1, 2, 0])
    # `to_categorical` converts this into a matrix with as many
    # columns as there are classes. The number of rows
    # stays the same.
    > to_categorical(labels)
    array([[ 1.,  0.,  0.],
           [ 0.,  0.,  1.],
           [ 0.,  1.,  0.],
           [ 0.,  0.,  1.],
           [ 1.,  0.,  0.]], dtype=float32)
    ```
    """

    y = np.array(y, dtype='int')
    input_shape = y.shape
    if input_shape and input_shape[-1] == 1 and len(input_shape) > 1:
        input_shape = tuple(input_shape[:-1])
    y = y.ravel()
    if not num_classes:
        num_classes = np.max(y) + 1
    n = y.shape[0]
    categorical = np.zeros((n, num_classes), dtype=dtype)
    categorical[np.arange(n), y] = 1
    output_shape = input_shape + (num_classes,)
    categorical = np.reshape(categorical, output_shape)
    return categorical

def decategorize(categorized, origin_map):
    '''
    Convert categorized image(output of Snet) to normal image
    according to origin_map
    '''
    #TODO: generalize to number of channels of categorized images..
    h,w,n_classes = categorized.shape
    n_channels = len(next(iter(origin_map.values())))
    ret_img = np.zeros((h,w,n_channels))

    if n_classes == 3:
        img_b, img_g, img_r = np.rollaxis(categorized, axis=-1)
        for c in range(n_classes):
            category = to_categorical(c, n_classes)
            origin = origin_map[tuple(category)]

            key_b, key_g, key_r = category
            masks = ((img_b == key_b) 
                   & (img_g == key_g) 
                   & (img_r == key_r)) # if [0,0,0]
            ret_img[masks] = origin

    elif n_classes == 2:
        img_0, img_1 = np.rollaxis(categorized, axis=-1)
        for c in range(n_classes):
            category = to_categorical(c, n_classes)
            origin = origin_map[tuple(category)]

            key_0, key_1 = category
            masks = ((img_0 == key_0) 
                   & (img_1 == key_1)) # if [0,0,0]
            ret_img[masks] = origin

    elif n_classes == 4:
        img_0, img_1, img_2, img_3 = np.rollaxis(categorized, axis=-1)        
        for c in range(n_classes):
            category = to_categorical(c, n_classes)
            origin = origin_map[tuple(category)]

            key_0, key_1, key_2, key_3 = category
            masks = ((img_0 == key_0) 
                   & (img_1 == key_1) 
                   & (img_2 == key_2) 
                   & (img_3 == key_3)) # if [0,0,0]
            ret_img[masks] = origin

    return ret_img


if __name__ == '__main__':
    assert is_img_file('.') == False
    assert is_img_file('./test/bigimg.png') 
    
    #print(QImage('./test_imgs/test_project/masks/2900045.png').format())
