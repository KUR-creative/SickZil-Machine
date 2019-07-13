import os,sys
sys.path.append( os.path.abspath('../src') )

import pytest
import numpy as np
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QUrl
from pathlib import Path
import cv2

import utils.fp as fp
import gui
import state
import config
import core

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
         fpath('fixture/prj_3file_I',config.IMGDIR,'2'), 
         fpath('fixture/prj_3file_I',config.IMGDIR,'3'))
    ))
    expected_masks = tuple(fp.map(
        os.path.abspath,
        (fpath('fixture/prj_3file_I',config.MASKDIR,'1'), 
         fpath('fixture/prj_3file_I',config.MASKDIR,'2'), 
         fpath('fixture/prj_3file_I',config.MASKDIR,'3'))
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

def test_gen_segmap():
    main_window.open_project(QUrl(
        'file://' + os.path.abspath('./fixture/real_proj/')
    ))

    expected = core.segmap(cv2.imread(
        './fixture/real_proj/images/bgr1.png'))
    actual = main_window.gen_segmap()
    saved  = cv2.imread('./fixture/real_proj/masks/bgr1.png')

    assert np.array_equal(actual, expected)
    assert np.array_equal(saved, expected)

def test_gen_segmap_empty_state_then_no_action(clear_state):
    assert main_window.gen_segmap() is None
    # expected no error.

app.quit()
