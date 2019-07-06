import os,sys
sys.path.append( os.path.abspath('../src') )

import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QUrl
from pathlib import Path

import gui
import state
import config
import utils.fp as fp

app = QApplication(sys.argv)
main_window = gui.MainWindow(
    QQmlApplicationEngine()
)

@pytest.fixture
def clear_state():
    state.clear_all()

def assert_init_state():
    assert state.img_paths == ()
    assert state.cursor == 0

@pytest.mark.skip(reason="no way of currently testing this")
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

    assert state.img_paths == expected_imgs
    assert state.mask_paths == expected_masks
    assert dir_type == config.UNSUPPORT_DIR

def test_open_project_not_prjdir_nor_imgdir_then_no_state_change(clear_state):
    dir_type = main_window.open_project(QUrl(
        'file://' + os.path.abspath('./fixture')
    ))
    assert state.img_paths == () 
    assert state.mask_paths == () 
    assert dir_type == config.UNSUPPORT_DIR

def test_open_project_is_flat_imgdir_then_no_state_change(clear_state):
    flat_imgdir = str(Path('fixture/prj_3file_I', config.IMGDIR)) 
    dir_type = main_window.open_project(QUrl(
        'file://' + os.path.abspath(flat_imgdir)
    ))

    assert state.mask_paths == () 
    assert dir_type == config.FLAT_IMGDIR


app.quit()

'''
class TestGui(unittest.TestCase):
    def setUp(self):
        state.clear_all() 

    def tearDown(self):
        pass

    def assert_init_state(self):
        self.assertEqual(state.img_paths, ())
        self.assertEqual(state.cursor, 0)

    def test_open_project_with_prj3file_I_then_open_folder(self):
        self.assert_init_state()

        main_window.open_project(QUrl(
            'file://' + os.path.abspath('./fixture/prj_3file_I')
        ))

        self.assertEqual( 
            state.img_paths,
            tuple(fp.map(
                os.path.abspath,
                ('fixture/prj_3file_I/images/1', 
                 'fixture/prj_3file_I/images/2', 
                 'fixture/prj_3file_I/images/3'),
            ))
        )

    #def test_open_project_

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = gui.MainWindow(
        QQmlApplicationEngine()
    )

    unittest.main()

    app.quit()
'''
