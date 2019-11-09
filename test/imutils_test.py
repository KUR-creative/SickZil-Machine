import pytest
import os,sys
sys.path.append( os.path.abspath('../src') )

from utils import imutils as iu
from utils import futils as fu

def posix_abspath(path):
    abspath = os.path.abspath(path)
    return(abspath.replace('\\','/') if '\\' in abspath
      else abspath)

import platform


posix_fpath = posix_abspath("./fixture/한국어경로real/images/bgr1.png")
@pytest.mark.skipif(platform.system() == 'Linux'
    or not os.path.isfile(posix_fpath), 
    reason='Skipped due to file non-existent, or Operating System(not Windows)')
def test_imread_kor_posix_path():
    global posix_fpath
    img = iu.imread(posix_fpath)

window_fpath = 'C:/Users/KUR/Documents/카카오톡 받은 파일/새 폴더_mproj/masks/magi-2163285.png'
@pytest.mark.skipif(platform.system() == 'Linux'
    or not os.path.isfile(window_fpath),     
    reason='Skipped due to file non-existent, or Operating System(not Windows)')
def test_imread_kor_win_path():
    global window_fpath
    img = iu.imread(window_fpath)

@pytest.mark.skipif(
    not os.path.exists('./private_fixtures/broken_imghdr/'), 
    reason='If it skipped, add proper broken_imghdr in private_fixtures directory.')
def test_is_img_file__if_loadable_then_file_is_image():
    for path in fu.children('./private_fixtures/broken_imghdr/'):
        assert iu.is_img_file(path)
