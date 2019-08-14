# -*- coding: utf-8 -*-
import pytest
import os,sys
sys.path.append( os.path.abspath('../src') )

from pathlib import Path, PurePosixPath
import state
import utils.fp as fp
import consts

def test_new_project(tmpdir):
    imgdir = 'fixture/prj_3file_I/images'
    state.new_project(imgdir, tmpdir)

    assert(set(os.listdir(tmpdir))
        == set(['images','masks', 'prev_images','prev_masks']))
    assert (
        set(os.listdir(imgdir))
        .issuperset(set(os.listdir(tmpdir / 'images')))
    )

    assert(set(os.listdir(tmpdir / 'images'))
        == set(os.listdir(tmpdir / 'prev_images')))

def fpath(*ps): return str(PurePosixPath(*ps))
def fpath_real(*ps): return str(Path(*ps))
def test_set_project():
    prjdir = 'fixture/prj_3file_I/'
    state.set_project(prjdir)
    assert state.img_paths  == (
        fpath(prjdir, consts.IMGDIR,'1'), 
        fpath(prjdir, consts.IMGDIR,'2.png'), 
        fpath(prjdir, consts.IMGDIR,'3.jpg')
    )
    assert state.mask_paths == (
        fpath(prjdir, consts.MASKDIR,'1.png'), 
        fpath(prjdir, consts.MASKDIR,'2.png'), 
        fpath(prjdir, consts.MASKDIR,'3.png')
    )
    assert state.prev_img_paths  == (
        fpath_real(prjdir, consts.PREV_IMGDIR,'1'), 
        fpath_real(prjdir, consts.PREV_IMGDIR,'2.png'), 
        fpath_real(prjdir, consts.PREV_IMGDIR,'3.jpg')
    )
    assert state.prev_mask_paths == (
        fpath_real(prjdir, consts.PREV_MASKDIR,'1.png'), 
        fpath_real(prjdir, consts.PREV_MASKDIR,'2.png'), 
        fpath_real(prjdir, consts.PREV_MASKDIR,'3.png')
    )


def test_clear_all():
    state.set_project('fixture/prj_3file_I/')
    state.clear_all()
    assert state.project() == ((),())
    assert state.cursor() == 0

def test_dir_type():
    unsupport_dir = 'fixture'
    nowhere_dir = 'nowhere'
    flat_imgdir = str(Path('fixture/prj_3file_I', consts.IMGDIR)) 
    project_dir = 'fixture/prj_3file_I/'
    not_proj_no_prevs = 'fixture/not_proj_cuz_no_prevs/'

    assert state.dir_type(nowhere_dir) == consts.UNSUPPORT_DIR
    assert state.dir_type(unsupport_dir) == consts.UNSUPPORT_DIR
    assert state.dir_type(flat_imgdir) == consts.FLAT_IMGDIR
    assert state.dir_type(project_dir) == consts.PRJDIR
    # NOTE: version 0.1.0
    assert state.dir_type(not_proj_no_prevs) == consts.UNSUPPORT_DIR

def test_img_mask_pairs():
    state.set_project('fixture/prj_3file_I/')
    img_masks = state.img_mask_pairs()
    expected_pairs = [
        (fpath('fixture/prj_3file_I',consts.IMGDIR,'1'),
         fpath('fixture/prj_3file_I',consts.MASKDIR,'1.png')),
        (fpath('fixture/prj_3file_I',consts.IMGDIR,'2.png'),
         fpath('fixture/prj_3file_I',consts.MASKDIR,'2.png')),
        (fpath('fixture/prj_3file_I',consts.IMGDIR,'3.jpg'),
         fpath('fixture/prj_3file_I',consts.MASKDIR,'3.png')),
    ]
    for actual, (ipath,mpath) in zip(state.img_mask_pairs(),
                                     expected_pairs):
        assert actual.img  == ipath
        assert actual.mask == mpath

#----- unicode paths -----
def test_set_project_kor_path():
    prjdir = 'fixture/한국어경로3img/'
    state.set_project(prjdir)
    assert state.img_paths  == (
        fpath(prjdir, consts.IMGDIR,'1'), 
        fpath(prjdir, consts.IMGDIR,'2.png'), 
        fpath(prjdir, consts.IMGDIR,'3.jpg')
    )
    assert state.mask_paths == (
        fpath(prjdir, consts.MASKDIR,'1.png'), 
        fpath(prjdir, consts.MASKDIR,'2.png'), 
        fpath(prjdir, consts.MASKDIR,'3.png')
    )
    assert state.prev_img_paths  == (
        fpath_real(prjdir, consts.PREV_IMGDIR,'1'), 
        fpath_real(prjdir, consts.PREV_IMGDIR,'2.png'), 
        fpath_real(prjdir, consts.PREV_IMGDIR,'3.jpg')
    )
    assert state.prev_mask_paths == (
        fpath_real(prjdir, consts.PREV_MASKDIR,'1.png'), 
        fpath_real(prjdir, consts.PREV_MASKDIR,'2.png'), 
        fpath_real(prjdir, consts.PREV_MASKDIR,'3.png')
    )

@pytest.mark.skipif(
    not os.path.exists('./private_fixtures/broken_imghdr_partial/'), 
    reason='If it skipped, add proper broken_imghdr_partial in private_fixtures directory.')
def test_load_only_image_files(tmpdir):
    imgdir = './private_fixtures/broken_imghdr_partial/'
    state.new_project(imgdir, tmpdir)
    state.set_project(tmpdir)
    assert len(state.img_paths) == 3 # dependent to fixture..

'''
def test_clear_all():
    state.set_project('fixture/prj_3file_I/')
    state.clear_all()
    assert state.project() == ((),())
    assert state.cursor() == 0

def test_dir_type():
    unsupport_dir = 'fixture'
    nowhere_dir = 'nowhere'
    flat_imgdir = str(Path('fixture/prj_3file_I', consts.IMGDIR)) 
    project_dir = 'fixture/prj_3file_I/'
    not_proj_no_prevs = 'fixture/not_proj_cuz_no_prevs/'

    assert state.dir_type(nowhere_dir) == consts.UNSUPPORT_DIR
    assert state.dir_type(unsupport_dir) == consts.UNSUPPORT_DIR
    assert state.dir_type(flat_imgdir) == consts.FLAT_IMGDIR
    assert state.dir_type(project_dir) == consts.PRJDIR
    # NOTE: version 0.1.0
    assert state.dir_type(not_proj_no_prevs) == consts.UNSUPPORT_DIR

def test_img_mask_pairs():
    state.set_project('fixture/prj_3file_I/')
    img_masks = state.img_mask_pairs()
    expected_pairs = [
        (fpath('fixture/prj_3file_I',consts.IMGDIR,'1'),
         fpath('fixture/prj_3file_I',consts.MASKDIR,'1.png')),
        (fpath('fixture/prj_3file_I',consts.IMGDIR,'2.png'),
         fpath('fixture/prj_3file_I',consts.MASKDIR,'2.png')),
        (fpath('fixture/prj_3file_I',consts.IMGDIR,'3.jpg'),
         fpath('fixture/prj_3file_I',consts.MASKDIR,'3.png')),
    ]
    for actual, (ipath,mpath) in zip(state.img_mask_pairs(),
                                     expected_pairs):
        assert actual.img  == ipath
        assert actual.mask == mpath
'''
