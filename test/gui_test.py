import os,sys
sys.path.append( os.path.abspath('../src') )

from pathlib import Path, PurePosixPath
import shutil
import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QUrl
import numpy as np
import cv2

import utils.fp as fp
import utils.futils as fu
import gui
import state
import consts
consts.load_config()
import core
import imgio as io

app = QApplication(sys.argv)
main_window = gui.MainWindow(
    QQmlApplicationEngine()
)

@pytest.fixture
def clear_state():
    state.clear_all()

def fpath(*ps): 
    return str(PurePosixPath(*ps))
def posix_abspath(path):
    abspath = os.path.abspath(path)
    return(abspath.replace('\\','/') if '\\' in abspath
      else abspath)

def open_project(prjdir):
    abspath = os.path.abspath(prjdir)
    main_window.open_project(QUrl(
        'file://' + '/' + abspath.replace('\\','/') if '\\' in abspath
        else 'file://' + abspath
    ))

#@pytest.mark.skip(reason="no way of currently testing this")
def test_open_project_with_prj3file_then_open_folder(clear_state):
    open_project('./fixture/prj_3file_I')

    expected_imgs = tuple(fp.map(
        posix_abspath,
        (fpath('fixture/prj_3file_I',consts.IMGDIR,'1'), 
         fpath('fixture/prj_3file_I',consts.IMGDIR,'2.png'), 
         fpath('fixture/prj_3file_I',consts.IMGDIR,'3.jpg'))
    ))
    expected_masks = tuple(fp.map(
        posix_abspath,
        (fpath('fixture/prj_3file_I',consts.MASKDIR,'1.png'), 
         fpath('fixture/prj_3file_I',consts.MASKDIR,'2.png'), 
         fpath('fixture/prj_3file_I',consts.MASKDIR,'3.png'))
    ))

    assert state.project() == (expected_imgs,expected_masks)

def test_open_project_not_prjdir_nor_imgdir_then_no_state_change(clear_state):
    open_project('./fixture')
    assert state.project() == ((),())

def test_open_project_is_flat_imgdir_then_no_state_change(clear_state):
    open_project('fixture/prj_3file_I/' + consts.IMGDIR)
    assert state.project() == ((),())

def test_gen_mask():
    open_project('./fixture/real_proj/')
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

def test_no_img_then_nothing_happen_when_calling_rm_txt_all(clear_state):
    assert fp.is_empty( main_window.rm_txt_all() )

def test_all_imgs_have_mask_then_rm_txt_all_just_load_masks(clear_state):
    open_project('./fixture/all_have_masks/')
    prev_masks = fp.lmap(cv2.imread, state.mask_paths)
    main_window.rm_txt_all()

    # Do not overwrite previously saved masks
    now_masks = fp.lmap(cv2.imread, state.mask_paths)
    for prev_mask,now_mask in zip(prev_masks,now_masks):
        assert np.array_equal(prev_mask,now_mask)

def test_if_some_imgs_hasnt_mask_then_generate_mask_for_them_in_rm_txt_all(clear_state):
    open_project('./fixture/some_hasnt_mask/')
    saved_mpaths = fp.lfilter( 
        lambda p: Path(p).exists(), state.mask_paths )
    main_window.rm_txt_all()
    mpaths = fp.lfilter( 
        lambda p: Path(p).exists(), state.mask_paths )

    assert len(saved_mpaths) < len(mpaths)

    # NOTE: Below could be problematic testing code.. Use mock instead..
    generated_mpaths = set(mpaths) - set(saved_mpaths)
    for mask_path in generated_mpaths:
        os.remove(mask_path)

def test_restore_prev_image_copy_img_from_prev_images_to_images(clear_state, tmpdir_factory):
    # Create fixture
    tmp_proj = tmpdir_factory.mktemp('tmp_proj')
    shutil.rmtree(tmp_proj) # dst dir must not exist for copytree
    shutil.copytree('./fixture/real_proj/', tmp_proj)

    open_project(tmp_proj)

    main_window.rm_txt_all()
    prev_img  = io.load(state.prev_image(),io.IMAGE)
    processed = io.load(state.now_image(), io.IMAGE)
    assert np.any(np.not_equal( processed, prev_img ))

    main_window.restore_prev_image()
    restored = io.load(state.now_image(), io.IMAGE)
    assert np.array_equal( restored, prev_img )

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
