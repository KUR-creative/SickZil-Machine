#TODO: save mask & image in `png` format!
#      and warn it to user: converted to png..
#      (After conversion, all jpgs are deleted)
from pathlib import Path
from collections import namedtuple
import shutil
import funcy as F

import config
import utils.fp as fp
import utils.imutils as iu
import utils.futils as fu

# NOTE: DO NOT ASSIGN DIRECTLY!
img_paths = () 
mask_paths= ()
prev_img_paths = () 
prev_mask_paths= ()
_cursor = 0 # NOTE: private! DO NOT ACCESS!!!!

#-----------------------------------------------
def now_image():
    global img_paths, _cursor
    if img_paths:
        return img_paths[_cursor]

def now_mask():
    global mask_paths, _cursor
    if mask_paths:
        return mask_paths[_cursor]

def project():
    global img_paths, mask_paths
    return namedtuple(
        'Project', 
        'img_paths mask_paths')(
         img_paths,mask_paths
    )

def img_mask_pairs():
    global img_paths, mask_paths
    return F.tap(tuple(fp.map(
        namedtuple('PathPair', 'img mask'),
        img_paths, mask_paths
    )))

#-----------------------------------------------
def new_project(imgdir, projdir):
    # create folder structure
    Path(projdir, config.IMGDIR).mkdir(parents=True, exist_ok=True)
    Path(projdir, config.MASKDIR).mkdir(parents=True, exist_ok=True)
    Path(projdir, config.PREV_IMGDIR).mkdir(parents=True, exist_ok=True)
    Path(projdir, config.PREV_MASKDIR).mkdir(parents=True, exist_ok=True)
    # copy imgs
    imgpaths = filter(iu.is_img_file, fu.children(imgdir))
    for imgpath in imgpaths:
        shutil.copy( str(imgpath), Path(projdir, config.IMGDIR))
        shutil.copy( str(imgpath), Path(projdir, config.PREV_IMGDIR))
    return projdir

def set_project(prj_dirpath):
    assert Path(prj_dirpath, config.IMGDIR).exists()
    assert Path(prj_dirpath, config.MASKDIR).exists()
    assert Path(prj_dirpath, config.PREV_IMGDIR).exists()
    assert Path(prj_dirpath, config.PREV_MASKDIR).exists()

    global img_paths, mask_paths,\
           prev_img_paths, prev_mask_paths, _cursor

    img_paths = fp.go(
        Path(prj_dirpath) / config.IMGDIR,
        fu.children, 
        fp.filter(iu.is_img_file),
        fu.human_sorted, 
        tuple
    )
    mask_paths = tuple(fp.map(
        fp.pipe(
            fu.replace1(config.IMGDIR, config.MASKDIR),
            Path, lambda p:p.with_suffix('.png'), str 
        ),
        img_paths
    ))

    prev_img_paths = tuple(fp.map(
        fu.replace1(config.IMGDIR, config.PREV_IMGDIR),
        img_paths
    ))
    prev_mask_paths = tuple(fp.map(
        fu.replace1(config.MASKDIR, config.PREV_MASKDIR),
        mask_paths
    ))

    _cursor = 0

def clear_all():
    global img_paths, mask_paths, _cursor
    img_paths = ()
    mask_paths = ()
    _cursor = 0

def cursor(new=None):
    global _cursor
    if new is None: # getter
        return _cursor
    elif img_paths: # setter
        _cursor = new % len(img_paths)

def next():
    global _cursor
    cursor(_cursor + 1)
def prev():
    global _cursor
    cursor(_cursor - 1)

#-----------------------------------------------
# NOTE: if project structure changed in future,
# maybe need some X_X_X version directory type
# for backward compatibility.
def dir_type(dirpath):
    parent = Path(dirpath)

    prjdir = ((parent / config.IMGDIR).exists()
          and (parent / config.MASKDIR).exists()
          and (parent / config.PREV_IMGDIR).exists()
          and (parent / config.PREV_MASKDIR).exists())
    imgdir = any(fp.map(
        iu.is_img_file, fu.children(parent)
    ))

    return(config.PRJDIR      if prjdir 
      else config.FLAT_IMGDIR if imgdir 
      else config.UNSUPPORT_DIR)
