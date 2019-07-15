import os,sys
sys.path.append( os.path.abspath('../src') )

import core
import cv2

def test_segment_input_output_spec_check():
    img1 = cv2.imread('./fixture/real_proj/images/bw1.png')
    img2 = cv2.imread('./fixture/real_proj/images/bgr1.png')
    ret1 = core.segmap(img1)
    ret2 = core.segmap(img2)

    # look & feel TODO:turn on..
    #cv2.imshow('img1',img1); cv2.imshow('img2',img2);
    #cv2.imshow('ret1',ret1); cv2.imshow('ret2',ret2);
    #cv2.waitKey(0)

# test different data(robustness)
def test_inpainted_input_output_spec_check():
    img1 = cv2.imread('./fixture/real_proj/images/bw1.png')
    img2 = cv2.imread('./fixture/real_proj/images/bgr1.png')
    seg1 = core.segmap(img1)
    seg2 = core.segmap(img2)
    ret1 = core.inpainted(img1,seg1)
    ret2 = core.inpainted(img2,seg2)

    # look & feel TODO:turn on..
    #cv2.imshow('img1',img1); cv2.imshow('img2',img2);
    #cv2.imshow('seg1',seg1); cv2.imshow('seg2',seg2);
    #cv2.imshow('ret1',ret1); cv2.imshow('ret2',ret2);
    #cv2.waitKey(0)
