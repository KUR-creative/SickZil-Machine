STARTUP_IMAGE = '../resource/startup.png'

###### DO NOT CHANGE BELOW! ######
MAIN_CONTEXT_NAME = 'main'
MAIN_QML = '../qml/szmc-0.1.0.qml'

IMGDIR = 'images'
MASKDIR = 'masks'

# open_project(TYPE)s
FLAT_IMGDIR = 'flat_imgdir'
UNSUPPORT_DIR= 'unsupport_dir'
PRJDIR = 'prjdir'

WARN_MSGS = {
    UNSUPPORT_DIR:'This is neither project nor image folder.',
    FLAT_IMGDIR: "it's img directory. not yet implemented!",
}

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
