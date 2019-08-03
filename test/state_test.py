import os,sys
sys.path.append( os.path.abspath('../src') )

from pathlib import Path
import state
import utils.fp as fp
import config

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

def test_set_project():
    prjdir = 'fixture/prj_3file_I/'
    state.set_project(prjdir)
    def fpath(*ps): return str(Path(*ps))
    assert state.img_paths  == (
        fpath(prjdir, config.IMGDIR,'1'), 
        fpath(prjdir, config.IMGDIR,'2.png'), 
        fpath(prjdir, config.IMGDIR,'3.jpg')
    )
    assert state.mask_paths == (
        fpath(prjdir, config.MASKDIR,'1.png'), 
        fpath(prjdir, config.MASKDIR,'2.png'), 
        fpath(prjdir, config.MASKDIR,'3.png')
    )
    assert state.prev_img_paths  == (
        fpath(prjdir, config.PREV_IMGDIR,'1'), 
        fpath(prjdir, config.PREV_IMGDIR,'2.png'), 
        fpath(prjdir, config.PREV_IMGDIR,'3.jpg')
    )
    assert state.prev_mask_paths == (
        fpath(prjdir, config.PREV_MASKDIR,'1.png'), 
        fpath(prjdir, config.PREV_MASKDIR,'2.png'), 
        fpath(prjdir, config.PREV_MASKDIR,'3.png')
    )


def test_clear_all():
    state.set_project('fixture/prj_3file_I/')
    state.clear_all()
    assert state.project() == ((),())
    assert state.cursor() == 0

def test_dir_type():
    def fpath(*ps): return str(Path(*ps))
    unsupport_dir = 'fixture'
    nowhere_dir = 'nowhere'
    flat_imgdir = str(Path('fixture/prj_3file_I', config.IMGDIR)) 
    project_dir = 'fixture/prj_3file_I/'
    not_proj_no_prevs = 'fixture/not_proj_cuz_no_prevs/'

    assert state.dir_type(nowhere_dir) == config.UNSUPPORT_DIR
    assert state.dir_type(unsupport_dir) == config.UNSUPPORT_DIR
    assert state.dir_type(flat_imgdir) == config.FLAT_IMGDIR
    assert state.dir_type(project_dir) == config.PRJDIR
    # NOTE: version 0.1.0
    assert state.dir_type(not_proj_no_prevs) == config.UNSUPPORT_DIR

def test_img_mask_pairs():
    state.set_project('fixture/prj_3file_I/')
    def fpath(*ps): return str(Path(*ps))
    img_masks = state.img_mask_pairs()
    expected_pairs = [
        (fpath('fixture/prj_3file_I',config.IMGDIR,'1'),
         fpath('fixture/prj_3file_I',config.MASKDIR,'1.png')),
        (fpath('fixture/prj_3file_I',config.IMGDIR,'2.png'),
         fpath('fixture/prj_3file_I',config.MASKDIR,'2.png')),
        (fpath('fixture/prj_3file_I',config.IMGDIR,'3.jpg'),
         fpath('fixture/prj_3file_I',config.MASKDIR,'3.png')),
    ]
    for actual, (ipath,mpath) in zip(state.img_mask_pairs(),
                                     expected_pairs):
        assert actual.img  == ipath
        assert actual.mask == mpath
