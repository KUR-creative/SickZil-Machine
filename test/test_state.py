import os,sys
sys.path.append( os.path.abspath('../src') )

from pathlib import Path
import state
import utils.fp as fp

def test_set_project():
    state.set_project('fixture/prj_3file_I/')
    assert state.img_paths  == ('fixture/prj_3file_I/images/1', 
                                'fixture/prj_3file_I/images/2', 
                                'fixture/prj_3file_I/images/3')
    assert state.mask_paths == ('fixture/prj_3file_I/masks/1', 
                                'fixture/prj_3file_I/masks/2', 
                                'fixture/prj_3file_I/masks/3')

def test_clear_all():
    state.set_project('fixture/prj_3file_I/')
    state.clear_all()
    assert state.img_paths  == () 
    assert state.mask_paths == () 

if __name__ == '__main__':
    unittest.main()
