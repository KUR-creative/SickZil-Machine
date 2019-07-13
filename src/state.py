from pathlib import Path
from collections import namedtuple
import funcy as F

import config
import utils.fp as fp
import utils.imutils as iu
import utils.futils as fu

# NOTE: DO NOT ASSIGN DIRECTLY!
img_paths = () 
mask_paths= ()
_cursor = 0 # NOTE: private! DO NOT ACCESS!!!!

def cursor(new=None):
    global _cursor
    if new is None: # getter
        return _cursor
    elif img_paths: # setter
        _cursor = new % len(img_paths)

def next():
    global _cursor
    if img_paths:
        _cursor = (_cursor + 1) % len(img_paths)
def prev():
    global _cursor
    if img_paths:
        _cursor = (_cursor - 1) % len(img_paths)

def project():
    global img_paths, mask_paths, _cursor
    return namedtuple(
        'Project', 
        'img_paths mask_paths')(
         img_paths,mask_paths
    )

def dir_type(dirpath):
    parent = Path(dirpath)

    prjdir = ((parent / config.IMGDIR).exists()
          and (parent / config.MASKDIR).exists())
    imgdir = any(fp.map(
        iu.is_img_file, fu.children(parent)
    ))

    return(config.PRJDIR      if prjdir 
      else config.FLAT_IMGDIR if imgdir 
      else config.UNSUPPORT_DIR)

def now_image():
    global img_paths, _cursor
    if img_paths:
        return img_paths[_cursor]

def now_mask():
    global mask_paths, _cursor
    if mask_paths:
        return mask_paths[_cursor]

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
