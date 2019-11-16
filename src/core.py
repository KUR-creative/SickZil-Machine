import os
import consts
os.environ['TF_CPP_MIN_LOG_LEVEL'] = consts.TF_CPP_MIN_LOG_LEVEL
# NOTE: above only work before tf was imported.
import tensorflow as tf
import numpy as np
import utils.imutils as iu
import utils.fp as fp

seg_limit = 4000000 # dev-machine: state, and init with user info...
compl_limit = 657666 #  then.. what is the optimal size?
def set_limits(slimit, climit):
    global seg_limit, compl_limit
    seg_limit = slimit # dev-machine: state, and init with user info...
    compl_limit = climit #  then.. what is the optimal size?

def load_model(mpath, version):
    #graph_def = tf.GraphDef()
    graph_def = tf.compat.v1.GraphDef()
    #with tf.gfile.GFile(mpath, 'rb') as f:
    with tf.io.gfile.GFile(mpath, 'rb') as f:
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(
            graph_def, 
            name = consts.model_name(mpath, version)
        )
load_model(consts.SNETPATH, '0.1.0')
load_model(consts.CNETPATH, '0.1.0')

#----------------------------------------------------------------
def segment_or_oom(segnet, inp, modulo=16):
    ''' If image is too big, return None '''
    h,w = inp.shape[:2]

    img = iu.modulo_padded(inp, modulo) 
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

def segment(segnet, inp, modulo=16):
    ''' oom-free segmentation '''
    global seg_limit
    
    h,w = inp.shape[:2] # 1 image, not batch.
    result = None
    if h*w < seg_limit:
        result = segment_or_oom(segnet, inp, modulo)
        if result is None: # seg_limit: Ok but OOM occur!
            seg_limit = h*w
            #print('segmentation seg_limit =', seg_limit, 'updated!')
    #else:
        #print('segmentation seg_limit exceed! img_size =', 
              #h*w, '>', seg_limit, '= seg_limit')

    if result is None: # exceed seg_limit or OOM
        if h > w:
            upper = segment(segnet, inp[:h//2,:], modulo) 
            downer= segment(segnet, inp[h//2:,:], modulo)
            return np.concatenate((upper,downer), axis=0)
        else:
            left  = segment(segnet, inp[:,:w//2], modulo)
            right = segment(segnet, inp[:,w//2:], modulo)
            return np.concatenate((left,right), axis=1)
    #print('segmented', result.shape)
    return result # image segmented successfully!

def segmap(image):
    '''
    return: uint8 mask image, bg=black.

    If image is not float32 nor bgr-3channel image, convert it.
    But snet input img(float32) pixel range: 0 ~ 1 is mandatory.
    '''
    def assert_img_range(img):
        assert (1.0 >= img).all(), img.max()
        assert (img >= 0.0).all(), img.min()
        return img
    def decategorize(mask): 
        return iu.decategorize(mask, iu.rgb2wk_map)

    with tf.compat.v1.Session() as sess:
        snet_in  = consts.snet_in('0.1.0', sess)
        snet_out = consts.snet_out('0.1.0', sess)
        def snet(img): 
            return sess.run(snet_out, feed_dict={snet_in:img})

        return fp.go(
            image,
            iu.channel3img, iu.float32, # preprocess
            assert_img_range,
            lambda img: segment(snet,img),
            iu.map_max_row, decategorize, iu.uint8, # postprocess
        )
#----------------------------------------------------------------
# Completion Network
def inpaint_or_oom(complnet, image, segmap):
    ''' If image is too big, return None '''
    #mask = binarization(segmap, 127) # 255 / 2 # maybe useless.
    mask = segmap
    assert image.shape == mask.shape 

    h,w = image.shape[:2] # 1 image, not batch.

    image = iu.modulo_padded(image,8)
    mask  = iu.modulo_padded(mask,8)

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
def inpaint(complnet, img, mask):
    ''' oom-free inpainting '''
    global compl_limit

    h,w = img.shape[:2]
    result = None
    if h*w < compl_limit:
        result = inpaint_or_oom(complnet, img, mask)
        if result is None: # compl_limit: Ok but OOM occur!
            compl_limit = h*w
    #else:
        #print('compl_limit exceed! img_size =', 
              #h*w, '>', compl_limit, '= compl_limit')

    if result is None: # exceed compl_limit or OOM
        if h > w:
            upper = inpaint(complnet, img[:h//2,:], mask[:h//2,:]) 
            downer= inpaint(complnet, img[h//2:,:], mask[h//2:,:])
            return np.concatenate((upper,downer), axis=0)
        else:
            left  = inpaint(complnet, img[:,:w//2], mask[:,:w//2])
            right = inpaint(complnet, img[:,w//2:], mask[:,w//2:])
            return np.concatenate((left,right), axis=1)
    #print('inpainted', result.shape)
    return result # image inpainted successfully!

def inpainted(image, segmap):
    '''
    return: uint8 text removed image.

    image:  uint8 bgr manga image.
    segmap: uint8 bgr mask image, bg=black.
    '''
    assert (255 >= image).all(), image.max()
    assert   (image >= 0).all(), image.min()
    with tf.compat.v1.Session() as sess:
        cnet_in  = consts.cnet_in('0.1.0',sess)
        cnet_out = consts.cnet_out('0.1.0',sess)
        return inpaint(
            lambda img:sess.run(
                cnet_out, feed_dict={cnet_in:img}
            ), 
            image, segmap
        )
