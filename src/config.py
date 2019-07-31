STARTUP_IMAGE = '../resource/startup.png'

###### DO NOT CHANGE BELOW! ######
MAIN_CONTEXT_NAME = 'main'
MAIN_QML = '../qml/szmc-0.1.0.qml'

IMGDIR = 'images'
MASKDIR = 'masks'
ORIGIN_IMGDIR = 'origin_' + IMGDIR
ORIGIN_MASKDIR = 'origin_' + MASKDIR

# core config
#TF_CPP_MIN_LOG_LEVEL = '1' #'3'
TF_CPP_MIN_LOG_LEVEL = '3'
SNETPATH = '../resource/snet/snet-0.1.0.pb'
CNETPATH = '../resource/cnet/cnet-0.1.0.pb'
#TODO: it.. has.. some... smell...
def model_name(mpath, version):
    return {
        '0.1.0': 'snet' if mpath == SNETPATH else ''
    }[version]

def snet_in(version, sess):
    return {
        '0.1.0': sess.graph.get_tensor_by_name('snet/input_1:0')
    }[version]
def snet_out(version, sess):
    return {
        '0.1.0': sess.graph.get_tensor_by_name('snet/conv2d_19/truediv:0')
    }[version]

def cnet_in(version, sess):
    return {
        '0.1.0': sess.graph.get_tensor_by_name('INPUT:0')
    }[version]
def cnet_out(version, sess):
    return {
        '0.1.0': sess.graph.get_tensor_by_name('OUTPUT:0')
    }[version]

# open_project(TYPE)s
FLAT_IMGDIR = 'flat_imgdir'
UNSUPPORT_DIR= 'unsupport_dir'
PRJDIR = 'prjdir'

WARN_MSGS = {
    UNSUPPORT_DIR:'This is neither project nor image folder.',
    FLAT_IMGDIR: "it's img directory. not yet implemented!",
}

def default_proj_name(imgdir_name):
    return imgdir_name + "_mproj"
'''
from collections import namedtuple

WarnMsgs = namedtuple('WarnMsgs',[FLAT_IMGDIR,UNSUPPORT_DIR,])
WARN_MSGS = Warn_msgs(
    UNSUPPORT_DIR ='This is neither project nor image folder.',
    FLAT_IMGDIR =  "it's img directory. not yet implemented!",
)

WARN_MSGS.UNSUPPORT_DIR = 1 <- how to do it?
print(WARN_MSGS.UNSUPPORT_DIR)
'''
