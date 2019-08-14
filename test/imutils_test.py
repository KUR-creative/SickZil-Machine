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
@pytest.mark.skipif(platform.system() == 'Linux', 
    reason='only for LAB MACHINE, Windows.')
def test_imread_kor_path():
    path = posix_abspath(
        "./fixture/한국어경로real/images/bgr1.png")
    img = iu.imread(path)
    path = 'C:/Users/KUR/Documents/카카오톡 받은 파일/새 폴더_mproj/masks/magi-2163285.png'
    img = iu.imread(path)

@pytest.mark.skipif(
    not os.path.exists('./private_fixtures/broken_imghdr/'), 
    reason='If it skipped, add proper broken_imghdr in private_fixtures directory.')
def test_is_img_file__if_loadable_then_file_is_image():
    for path in fu.children('./private_fixtures/broken_imghdr/'):
        assert iu.is_img_file(path)
