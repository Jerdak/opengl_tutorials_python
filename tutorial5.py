#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" Tutorial 5: Textured Cube
"""

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

import common
import glfw
import sys
import os

# Global window
window = None
null = c_void_p(0)

def opengl_init():
    global window
    # Initialize the library
    if not glfw.init():
        print("Failed to initialize GLFW\n",file=sys.stderr)
        return False

    # Open Window and create its OpenGL context
    window = glfw.create_window(1024, 768, "Tutorial 05", None, None) #(in the accompanying source code this variable will be global)
    glfw.window_hint(glfw.SAMPLES, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    if not window:
        print("Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible. Try the 2.1 version of the tutorials.\n",file=sys.stderr)
        glfw.terminate()
        return False

    # Initialize GLEW
    glfw.make_context_current(window)
    glewExperimental = True

    # GLEW is a framework for testing extension availability.  Please see tutorial notes for
    # more information including why can remove this code.
    if glewInit() != GLEW_OK:
        print("Failed to initialize GLEW\n",file=sys.stderr);
        return False
    return True

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

def main():
    if not opengl_init():
        return

    # Enable key events
    glfw.set_input_mode(window,glfw.STICKY_KEYS,GL_TRUE) 
    
    # Set opengl clear color to something other than red (color used by the fragment shader)
    glClearColor(0.0,0.0,0.4,0.0)
    
    # Enable depth test
    glEnable(GL_DEPTH_TEST);
    # Accept fragment if it closer to the camera than the former one
    glDepthFunc(GL_LESS); 

    vertex_array_id = glGenVertexArrays(1)
    glBindVertexArray( vertex_array_id )


    program_id = common.LoadShaders( ".\\shaders\\Tutorial5\\TransformVertexShader.vertexshader",
        ".\\shaders\\Tutorial5\\TextureFragmentShader.fragmentshader" )
    
    # Get a handle for our "MVP" uniform
    matrix_id = glGetUniformLocation(program_id, "MVP");

    # Projection matrix : 45 Field of View, 4:3 ratio, display range : 0.1 unit <-> 100 units
    projection = mat4.perspective(45.0, 4.0 / 3.0, 0.1, 100.0)
    
    # Camera matrix
    view = mat4.lookat(vec3(4,3,-3), # Camera is at (4,3,3), in World Space
                    vec3(0,0,0), # and looks at the origin
                    vec3(0,1,0)) 
    
    # Model matrix : an identity matrix (model will be at the origin)
    model = mat4.identity()

    # Our ModelViewProjection : multiplication of our 3 matrices
    mvp = projection * view * model


    texture = load_image(".\\content\\uvtemplate.bmp")
    texture_id  = glGetUniformLocation(program_id, "myTextureSampler")

    # Our vertices. Tree consecutive floats give a 3D vertex; Three consecutive vertices give a triangle.
    # A cube has 6 faces with 2 triangles each, so this makes 6*2=12 triangles, and 12*3 vertices
    vertex_data = [ 
        -1.0,-1.0,-1.0,
        -1.0,-1.0, 1.0,
        -1.0, 1.0, 1.0,
         1.0, 1.0,-1.0,
        -1.0,-1.0,-1.0,
        -1.0, 1.0,-1.0,
         1.0,-1.0, 1.0,
        -1.0,-1.0,-1.0,
         1.0,-1.0,-1.0,
         1.0, 1.0,-1.0,
         1.0,-1.0,-1.0,
        -1.0,-1.0,-1.0,
        -1.0,-1.0,-1.0,
        -1.0, 1.0, 1.0,
        -1.0, 1.0,-1.0,
         1.0,-1.0, 1.0,
        -1.0,-1.0, 1.0,
        -1.0,-1.0,-1.0,
        -1.0, 1.0, 1.0,
        -1.0,-1.0, 1.0,
         1.0,-1.0, 1.0,
         1.0, 1.0, 1.0,
         1.0,-1.0,-1.0,
         1.0, 1.0,-1.0,
         1.0,-1.0,-1.0,
         1.0, 1.0, 1.0,
         1.0,-1.0, 1.0,
         1.0, 1.0, 1.0,
         1.0, 1.0,-1.0,
        -1.0, 1.0,-1.0,
         1.0, 1.0, 1.0,
        -1.0, 1.0,-1.0,
        -1.0, 1.0, 1.0,
         1.0, 1.0, 1.0,
        -1.0, 1.0, 1.0,
         1.0,-1.0, 1.0]

    # Two UV coordinatesfor each vertex. They were created withe Blender.
    uv_data = [ 
        0.000059, 1.0-0.000004, 
        0.000103, 1.0-0.336048, 
        0.335973, 1.0-0.335903, 
        1.000023, 1.0-0.000013, 
        0.667979, 1.0-0.335851, 
        0.999958, 1.0-0.336064, 
        0.667979, 1.0-0.335851, 
        0.336024, 1.0-0.671877, 
        0.667969, 1.0-0.671889, 
        1.000023, 1.0-0.000013, 
        0.668104, 1.0-0.000013, 
        0.667979, 1.0-0.335851, 
        0.000059, 1.0-0.000004, 
        0.335973, 1.0-0.335903, 
        0.336098, 1.0-0.000071, 
        0.667979, 1.0-0.335851, 
        0.335973, 1.0-0.335903, 
        0.336024, 1.0-0.671877, 
        1.000004, 1.0-0.671847, 
        0.999958, 1.0-0.336064, 
        0.667979, 1.0-0.335851, 
        0.668104, 1.0-0.000013, 
        0.335973, 1.0-0.335903, 
        0.667979, 1.0-0.335851, 
        0.335973, 1.0-0.335903, 
        0.668104, 1.0-0.000013, 
        0.336098, 1.0-0.000071, 
        0.000103, 1.0-0.336048, 
        0.000004, 1.0-0.671870, 
        0.336024, 1.0-0.671877, 
        0.000103, 1.0-0.336048, 
        0.336024, 1.0-0.671877, 
        0.335973, 1.0-0.335903, 
        0.667969, 1.0-0.671889, 
        1.000004, 1.0-0.671847, 
        0.667979, 1.0-0.335851]

    vertex_buffer = glGenBuffers(1);
    array_type = GLfloat * len(vertex_data)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, len(vertex_data) * 4, array_type(*vertex_data), GL_STATIC_DRAW)

    uv_buffer = glGenBuffers(1);
    array_type = GLfloat * len(uv_data)
    glBindBuffer(GL_ARRAY_BUFFER, uv_buffer)
    glBufferData(GL_ARRAY_BUFFER, len(uv_data) * 4, array_type(*uv_data), GL_STATIC_DRAW)



    while glfw.get_key(window,glfw.KEY_ESCAPE) != glfw.PRESS and not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT)

        glUseProgram(program_id)

        # Send our transformation to the currently bound shader, 
        # in the "MVP" uniform
        glUniformMatrix4fv(matrix_id, 1, GL_FALSE,mvp.data)
        
        # Bind our texture in Texture Unit 0
        glActiveTexture(GL_TEXTURE0);
        glBindTexture(GL_TEXTURE_2D, texture);
        # Set our "myTextureSampler" sampler to user Texture Unit 0
        glUniform1i(texture_id, 0);

        #1rst attribute buffer : vertices
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer);
        glVertexAttribPointer(
            0,                  # attribute 0. No particular reason for 0, but must match the layout in the shader.
            3,                  # len(vertex_data)
            GL_FLOAT,           # type
            GL_FALSE,           # ormalized?
            0,                  # stride
            null                # array buffer offset (c_type == void*)
            )

        # 2nd attribute buffer : colors
        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, uv_buffer);
        glVertexAttribPointer(
            1,                  # attribute 0. No particular reason for 0, but must match the layout in the shader.
            2,                  # len(vertex_data)
            GL_FLOAT,           # type
            GL_FALSE,           # ormalized?
            0,                  # stride
            null                # array buffer offset (c_type == void*)
            )

        # Draw the triangle !
        glDrawArrays(GL_TRIANGLES, 0, 12*3) #3 indices starting at 0 -> 1 triangle

        # Not strictly necessary because we only have 
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
    
    
        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    # note braces around vertex_buffer and vertex_array_id.  
    # These 2 functions expect arrays of values
    glDeleteBuffers(1, [vertex_buffer])
    glDeleteBuffers(1, [uv_buffer])
    glDeleteProgram(program_id)
    glDeleteTextures([texture_id])
    glDeleteVertexArrays(1, [vertex_array_id])

    glfw.terminate()

if __name__ == "__main__":
    main()
