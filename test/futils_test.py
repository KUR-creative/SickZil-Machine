import pytest
from pathlib import Path

import os,sys
sys.path.append( os.path.abspath('../src') )
import utils.futils as fu

def test_delete_when_no_file():
    no_fpath = 'fixture/_NO_FILE_'
    file_deleted = fu.delete(no_fpath) # Nothing happens.

    assert file_deleted == False
    with pytest.raises(FileNotFoundError):
        fu.delete(no_fpath, except_on_fail=True) 

def test_delete_when_file_exist():
    tmp_path = 'fixture/temporary_file'
    Path(tmp_path).touch()

    assert Path(tmp_path).exists()
    file_deleted = fu.delete(tmp_path)
    assert not Path(tmp_path).exists()
    assert file_deleted
