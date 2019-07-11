import tensorflow as tf
import numpy as np
from imutils import binarization, modulo_padded
import os
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

# Segmentation Network
def load_model(model_path, is_snet=True):
    graph_def = tf.GraphDef()
    with tf.gfile.GFile(model_path, 'rb') as f:
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(
            graph_def, 
            name = 'snet' if is_snet else ''
        )

#def unload_model(): # Maybe useless
    #tf.reset_default_graph()

def segment_or_oom(segnet, inp, modulo=16):
    ''' If image is too big, return None '''
    h,w = inp.shape[:2]

    img = modulo_padded(inp, modulo) 
    img_bat = np.expand_dims(img,0) 
    segmap = segnet(img_bat)
    segmap = np.squeeze(segmap[:,:h,:w,:], 0) 
    return segmap
    '''
    try:
        img_bat = np.expand_dims(img,0) 
        segmap = segnet(img_bat)
        segmap = np.squeeze(segmap[:,:h,:w,:], 0) 
        return segmap
    except Exception as e: # ResourceExhaustedError:
        #print(traceback.print_tb(e.__traceback__)); exit()
        print(img.shape,'(Maybe) OOM error: image is too big. (in segnet)')
        return None
        '''

seg_limit = 4000000 # dev-machine: state, and init with user info...
def segment(segnet, inp, modulo=16):
    ''' oom-free segmentation '''
    global seg_limit
    
    h,w = inp.shape[:2] # 1 image, not batch.
    result = None
    if h*w < seg_limit:
        result = segment_or_oom(segnet, inp, modulo)
        if result is None: # seg_limit: Ok but OOM occur!
            seg_limit = h*w
            print('segmentation seg_limit =', seg_limit, 'updated!')
    else:
        print('segmentation seg_limit exceed! img_size =', 
              h*w, '>', seg_limit, '= seg_limit')

    if result is None: # exceed seg_limit or OOM
        if h > w:
            upper = segment(segnet, inp[:h//2,:], modulo) 
            downer= segment(segnet, inp[h//2:,:], modulo)
            return np.concatenate((upper,downer), axis=0)
        else:
            left  = segment(segnet, inp[:,:w//2], modulo)
            right = segment(segnet, inp[:,w//2:], modulo)
            return np.concatenate((left,right), axis=1)
    print('segmented', result.shape)
    return result # image segmented successfully!

# Completion Network
def inpaint_or_oom(complnet, image, segmap):
    ''' If image is too big, return None '''
    #mask = binarization(segmap, 127) # 255 / 2 # maybe useless.
    mask = segmap
    assert image.shape == mask.shape 

    h,w = image.shape[:2] # 1 image, not batch.

    image = modulo_padded(image,8)
    mask  = modulo_padded(mask,8)

    image = np.expand_dims(image, 0) # [h,w,c] -> [1,h,w,c]
    mask  = np.expand_dims(mask, 0)
    input_image = np.concatenate([image, mask], axis=2)

    result = complnet(input_image)
    return result[0][:h, :w, ::-1] #---------- remove padding
    '''
    try:
        result = complnet(input_image)
        return result[0][:h, :w, ::-1] #---------- remove padding
    except Exception as e: # ResourceExhaustedError:
        print((h,w), '(Maybe) OOM error while inpainting (in complnet)')
        return None
    '''

#compl_limit = 1525920 # it didn't crash, but SLOWER! why..?
#lab-machine #1525920
#compl_limit = 9999999 # 
compl_limit = 657666 #  then.. what is the optimal size?
def inpaint(complnet, img, mask):
    ''' oom-free inpainting '''
    global compl_limit

    h,w = img.shape[:2]
    result = None
    if h*w < compl_limit:
        result = inpaint_or_oom(complnet, img, mask)
        if result is None: # compl_limit: Ok but OOM occur!
            compl_limit = h*w
    else:
        print('compl_limit exceed! img_size =', 
              h*w, '>', compl_limit, '= compl_limit')

    if result is None: # exceed compl_limit or OOM
        if h > w:
            upper = inpaint(complnet, img[:h//2,:], mask[:h//2,:]) 
            downer= inpaint(complnet, img[h//2:,:], mask[h//2:,:])
            return np.concatenate((upper,downer), axis=0)
        else:
            left  = inpaint(complnet, img[:,:w//2], mask[:,:w//2])
            right = inpaint(complnet, img[:,w//2:], mask[:,w//2:])
            return np.concatenate((left,right), axis=1)
    print('inpainted', result.shape)
    return result # image inpainted successfully!

