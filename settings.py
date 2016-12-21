# -*- coding: utf-8 -*-
__author__ = 'yijingping'

DATABASE = {
        'HOST': '127.0.0.1',
        'NAME': 'poormining',
        'USER': 'root',
        'PASSWORD': '',
        'OPTIONS': {
            'charset': 'utf-8',
        }
}


## Import local settings
try:
    from settings import *
except ImportError:
    import sys, traceback
    sys.stderr.write("Warning: Can't find the file 'local_settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.stderr.write("\nFor debugging purposes, the exception was:\n\n")
    traceback.print_exc()