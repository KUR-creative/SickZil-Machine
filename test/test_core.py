import os,sys
sys.path.append( os.path.abspath('../src') )

import core
import cv2

def test_segment_input_output_spec_check():
    img = cv2.imread('../test/fixture/real_imgs/bw1.png')
    ret = core.segmap(img)

    # look & feel
    cv2.imshow('img',img)
    cv2.imshow('ret',ret)
    cv2.waitKey(0)

# test different data(robustness)
# test in multiple images
