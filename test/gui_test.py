import os,sys
sys.path.append( os.path.abspath('../src') )

import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QUrl
from pathlib import Path
import numpy as np
import cv2

import utils.fp as fp
import utils.futils as fu
import gui
import state
import config
import core
import imgio as io

app = QApplication(sys.argv)
main_window = gui.MainWindow(
    QQmlApplicationEngine()
)

@pytest.fixture
def clear_state():
    state.clear_all()

#@pytest.mark.skip(reason="no way of currently testing this")
def test_open_project_with_prj3file_then_open_folder(clear_state):
    dir_type = main_window.open_project(QUrl(
        'file://' + os.path.abspath('./fixture/prj_3file_I')
    ))

    def fpath(*ps): return str(Path(*ps))
    expected_imgs = tuple(fp.map(
        os.path.abspath,
        (fpath('fixture/prj_3file_I',config.IMGDIR,'1'), 
         fpath('fixture/prj_3file_I',config.IMGDIR,'2.png'), 
         fpath('fixture/prj_3file_I',config.IMGDIR,'3.jpg'))
    ))
    expected_masks = tuple(fp.map(
        os.path.abspath,
        (fpath('fixture/prj_3file_I',config.MASKDIR,'1.png'), 
         fpath('fixture/prj_3file_I',config.MASKDIR,'2.png'), 
         fpath('fixture/prj_3file_I',config.MASKDIR,'3.png'))
    ))

    assert state.project() == (expected_imgs,expected_masks)
    assert dir_type == config.PRJDIR

def test_open_project_not_prjdir_nor_imgdir_then_no_state_change(clear_state):
    dir_type = main_window.open_project(QUrl(
        'file://' + os.path.abspath('./fixture')
    ))
    assert state.project() == ((),())
    assert dir_type == config.UNSUPPORT_DIR

def test_open_project_is_flat_imgdir_then_no_state_change(clear_state):
    flat_imgdir = str(Path('fixture/prj_3file_I', config.IMGDIR)) 
    dir_type = main_window.open_project(QUrl(
        'file://' + os.path.abspath(flat_imgdir)
    ))

    assert state.project() == ((),())
    assert dir_type == config.FLAT_IMGDIR

def test_gen_mask():
    main_window.open_project(QUrl(
        'file://' + os.path.abspath('./fixture/real_proj/')
    ))

    expected = fp.go(
        './fixture/real_proj/images/bgr1.png',
        cv2.imread, core.segmap, io.segmap2mask
    )
    main_window.gen_mask()
    actual = cv2.imread(
        './fixture/real_proj/masks/bgr1.png',
        cv2.IMREAD_UNCHANGED) #NOTE: rgba -> 4channel, wb -> 1ch..

    assert np.array_equal(actual, expected)

def test_gen_mask_empty_state_then_no_action(clear_state):
    assert main_window.gen_mask() is None
    # expected no error.
# TODO: Add test
# gen_mask_all: ?
# rm_txt_all with existing mask: then use masks.
# rm_txt_all without mask: make segmaps and then use it.
# rm_txt with existing mask: then use mask.
# rm_txt without mask: make segmap and then use it.
# edit mask => gen segmap => add generated segmap to old mask
# edit mask(no mask) => rm_txt => ...

#NOTE: It's not testable(cuz no gui)! Find other way to test!
'''
def test_if_display_other_image_then_save_mask(clear_state):
    main_window.open_project(QUrl(
        'file://' + os.path.abspath('./fixture/real_proj/')
    ))
    mpath0 = state.now_mask()
    fu.delete(mpath0)
    assert not Path(mpath0).exists()

    # next
    main_window.display_next()
    print(mpath0)
    assert Path(mpath0).exists()
    # prev
    # goto some index
'''

app.quit()
