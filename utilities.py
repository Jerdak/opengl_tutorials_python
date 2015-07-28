#! /usr/bin/env python
""" Various Utilities
"""
from __future__ import print_function

from OpenGL.GL import *
from csgl import *

import glfw
import math as mathf

from PIL import Image
from PIL.Image import open as pil_open

def screenshot(file_name_out,width,height):
    data = glReadPixels(0,0,width,height,GL_RGB,GL_UNSIGNED_BYTE,outputType=None)
    image = Image.fromstring(mode="RGB", size=(width, height), data=data)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save(file_name_out)
