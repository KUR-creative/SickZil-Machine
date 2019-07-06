from pathlib import Path
import utils.fp as fp
import utils.futils as fu
import funcy as F

# DO NOT ASSIGN DIRECTLY!
img_paths = () 
mask_paths= ()
cursor = 0 # NOTE: private! DO NOT ACCESS!!!!

def set_project(prj_dirpath):
    global img_paths, mask_paths, cursor
    img_paths = fp.go(
        Path(prj_dirpath) / 'images',
        fu.children, 
        #F.tap,
        fu.human_sorted, 
        tuple
    )
    mask_paths = tuple(fp.map(
        fu.replace1('images', 'masks'),
        img_paths
    ))
    cursor = 0

def clear_all():
    global img_paths, mask_paths, cursor
    img_paths = ()
    mask_paths = ()
    cursor = 0
