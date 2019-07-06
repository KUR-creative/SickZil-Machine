import os,sys
sys.path.append( os.path.abspath('../src') )

import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QUrl
import gui
import state
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

def test_open_project_with_prj3file_then_open_folder(clear_state):
    main_window.open_project(QUrl(
        'file://' + os.path.abspath('./fixture/prj_3file_I')
    ))

    expected_imgs = tuple(fp.map(
        os.path.abspath,
        ('fixture/prj_3file_I/images/1', 
         'fixture/prj_3file_I/images/2', 
         'fixture/prj_3file_I/images/3'),
    ))
    expected_masks = tuple(fp.map(
        os.path.abspath,
        ('fixture/prj_3file_I/masks/1', 
         'fixture/prj_3file_I/masks/2', 
         'fixture/prj_3file_I/masks/3'),
    ))

    assert state.img_paths == expected_imgs
    assert state.mask_paths == expected_masks


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
