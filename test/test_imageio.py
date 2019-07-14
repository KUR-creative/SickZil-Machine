import os,sys
sys.path.append( os.path.abspath('../src') )

import cv2
import numpy as np
from PyQt5.QtGui import QImage
import imageio as io

def test_load():
    path = './fixture/real_proj/masks/bgr1.png'
    expected_qimg = QImage(path)
    expected_ndarr= cv2.imread(path, cv2.IMREAD_UNCHANGED)
    assert io.load(path) == expected_qimg
    assert np.array_equal(io.load(path,io.NDARR),expected_ndarr)
    assert np.array_equal(io.load(path,io.MASK),expected_ndarr)
