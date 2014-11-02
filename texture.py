#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from OpenGL.GL import *
from OpenGL.GL.ARB import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.special import *
from OpenGL.GL.shaders import *
from glew_wish import *
from csgl import *
from PIL.Image import open as pil_open

def bind_texture(texture_id,mode):
    """ Bind texture_id using several different modes

        Notes:
            Without mipmapping the texture is incomplete
            and requires additional constraints on OpenGL
            to properly render said texture.

            Use 'MIN_FILTER" or 'MAX_LEVEL' to render
            a generic texture with a single resolution
        Ref:
            [] - http://www.opengl.org/wiki/Common_Mistakes#Creating_a_complete_texture
            [] - http://gregs-blog.com/2008/01/17/opengl-texture-filter-parameters-explained/
        TODO:
            - Rename modes to something useful
    """
    if mode == 'DEFAULT':
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1) 
    elif mode == 'MIN_FILTER':
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1) 
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    elif mode == 'MAX_LEVEL':
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1) 
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
    else:
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)

    # Generate mipmaps?  Doesn't seem to work
    glGenerateMipmap(GL_TEXTURE_2D)

def load_image(file_name):
    im = pil_open(file_name)
    try:
        width,height,image = im.size[0], im.size[1], im.tostring("raw", "RGBA", 0, -1)
    except SystemError:
        width,height,image = im.size[0], im.size[1], im.tostring("raw", "RGBX", 0, -1)

    texture_id =  glGenTextures(1)

    # To use OpenGL 4.2 ARB_texture_storage to automatically generate a single mipmap layer
    # uncomment the 3 lines below.  Note that this should replaced glTexImage2D below.
    #bind_texture(texture_id,'DEFAULT')
    #glTexStorage2D(GL_TEXTURE_2D, 1, GL_RGBA8, width, height);
    #glTexSubImage2D(GL_TEXTURE_2D,0,0,0,width,height,GL_RGBA,GL_UNSIGNED_BYTE,image)
    
    # "Bind" the newly created texture : all future texture functions will modify this texture
    bind_texture(texture_id,'MIN_FILTER')
    glTexImage2D(
           GL_TEXTURE_2D, 0, 3, width, height, 0,
           GL_RGBA, GL_UNSIGNED_BYTE, image
       )
    return texture_id