from pathlib import Path
import funcy as F

import config
import utils.fp as fp
import utils.imutils as iu
import utils.futils as fu

# NOTE: DO NOT ASSIGN DIRECTLY!
img_paths = () 
mask_paths= ()
_cursor = 0 # NOTE: private! DO NOT ACCESS!!!!

def dir_type(dirpath):
    parent = Path(dirpath)

    prjdir = ((parent / 'images').exists()
          and (parent / 'masks').exists())
    imgdir = any(fp.map(
        iu.is_img_file, fu.children(parent)
    ))

    return(config.PRJDIR      if prjdir 
      else config.FLAT_IMGDIR if imgdir 
      else config.UNSUPPORT_DIR)

def set_project(prj_dirpath):
    assert Path(prj_dirpath,config.IMGDIR).exists()
    assert Path(prj_dirpath,config.MASKDIR).exists()

    global img_paths, mask_paths, _cursor
    img_paths = fp.go(
        Path(prj_dirpath) / config.IMGDIR,
        fu.children, 
        #F.tap,
        fu.human_sorted, 
        tuple
    )
    mask_paths = tuple(fp.map(
        fu.replace1(config.IMGDIR, config.MASKDIR),
        img_paths
    ))
    _cursor = 0

def clear_all():
    global img_paths, mask_paths, _cursor
    img_paths = ()
    mask_paths = ()
    _cursor = 0
