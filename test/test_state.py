import os,sys
sys.path.append( os.path.abspath('../src') )

from pathlib import Path
import state
import utils.fp as fp
import config

def test_set_project():
    state.set_project('fixture/prj_3file_I/')
    def fpath(*ps): return str(Path(*ps))
    assert state.img_paths  == (
        fpath('fixture/prj_3file_I',config.IMGDIR,'1'), 
        fpath('fixture/prj_3file_I',config.IMGDIR,'2'), 
        fpath('fixture/prj_3file_I',config.IMGDIR,'3')
    )
    assert state.mask_paths == (
        fpath('fixture/prj_3file_I',config.MASKDIR,'1'), 
        fpath('fixture/prj_3file_I',config.MASKDIR,'2'), 
        fpath('fixture/prj_3file_I',config.MASKDIR,'3')
    )

def test_clear_all():
    state.set_project('fixture/prj_3file_I/')
    state.clear_all()
    assert state.img_paths  == () 
    assert state.mask_paths == () 

if __name__ == '__main__':
    unittest.main()
