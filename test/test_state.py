import os,sys
sys.path.append( os.path.abspath('../src') )

from pathlib import Path
import state
import unittest
import utils.fp as fp

class TestState(unittest.TestCase):
    def test_set_init_set(self):
        state.set_project('fixture/prj_3file_I/')
        self.assertEqual( 
            state.img_paths,
            ('fixture/prj_3file_I/images/1', 
             'fixture/prj_3file_I/images/2', 
             'fixture/prj_3file_I/images/3')
        )
        self.assertEqual( 
            state.mask_paths,
            ('fixture/prj_3file_I/masks/1', 
             'fixture/prj_3file_I/masks/2', 
             'fixture/prj_3file_I/masks/3')
        )

if __name__ == '__main__':
    unittest.main()
