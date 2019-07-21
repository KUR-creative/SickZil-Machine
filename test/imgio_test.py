import os,sys
sys.path.append( os.path.abspath('../src') )

import cv2
from PyQt5.QtGui import QImage
import numpy as np
import imgio as io

def test_load():
    path = './fixture/not_proj_dir/bgr1_mask.png'
    expected_qimg = QImage(path)
    expected_ndarr= cv2.imread(path, cv2.IMREAD_UNCHANGED)
    assert io.load(path) == expected_qimg
    assert np.array_equal(io.load(path,io.NDARR),expected_ndarr)

def test_load_image():
    for path in ['./fixture/not_proj_dir/bgr1_mask.png',
                 './fixture/real_proj/images/bgr1.png',
                 './fixture/real_proj/images/bw1.png']:
        actual = io.load(path, io.IMAGE)
        expected = cv2.imread(path, cv2.IMREAD_COLOR)
        assert np.array_equal(actual,expected)

def test_load_mask():
    path = './fixture/not_proj_dir/bgr1_mask.png'
    h,w = cv2.imread(path, cv2.IMREAD_UNCHANGED).shape[:2]
    b,g,r = cv2.split(io.load(path,io.MASK))
    assert h == b.shape[0]
    assert w == g.shape[1]
    assert(np.array_equal(b,g) 
       and np.array_equal(g,r)
       and np.array_equal(r,b))
