#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" Tutorial 7: Model Loading
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
import controls
import objloader

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
    window = glfw.create_window(1024, 768, "Tutorial 07", None, None) #(in the accompanying source code this variable will be global)
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
    # more information including why can remove this code.a
    if glewInit() != GLEW_OK:
        print("Failed to initialize GLEW\n",file=stderropen.sys)
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
    #glTexStorage2D(GL_TEXTURE_2D, 1, GL_RGBA8, width, height)
    #glTexSubImage2D(GL_TEXTURE_2D,0,0,0,width,height,GL_RGBA,GL_UNSIGNED_BYTE,image)
    
    # "Bind" the newly created texture : all future texture functions will modify this texture
    bind_texture(texture_id,'MIN_FILTER')
    glTexImage2D(
           GL_TEXTURE_2D, 0, 3, width, height, 0,
           GL_RGBA, GL_UNSIGNED_BYTE, image
       )
    return texture_id

def main():

    # Initialize GLFW and open a window
    if not opengl_init():
        return

    # Enable key events
    glfw.set_input_mode(window,glfw.STICKY_KEYS,GL_TRUE) 
    glfw.set_cursor_pos(window, 1024/2, 768/2)

    # Set opengl clear color to something other than red (color used by the fragment shader)
    glClearColor(0.0,0.0,0.4,0.0)
    
    # Enable depth test
    glEnable(GL_DEPTH_TEST)

    # Accept fragment if it closer to the camera than the former one
    glDepthFunc(GL_LESS)

    # Cull triangles which normal is not towards the camera
    glEnable(GL_CULL_FACE)

    vertex_array_id = glGenVertexArrays(1)
    glBindVertexArray( vertex_array_id )

    # Create and compile our GLSL program from the shaders
    program_id = common.LoadShaders( ".\\shaders\\Tutorial7\\TransformVertexShader.vertexshader",
        ".\\shaders\\Tutorial7\\TextureFragmentShader.fragmentshader" )
    
    # Get a handle for our "MVP" uniform
    matrix_id = glGetUniformLocation(program_id, "MVP")

    # Load the texture
    texture = load_image(".\\content\\uvmap.bmp")

    # Get a handle for our "myTextureSampler" uniform
    texture_id  = glGetUniformLocation(program_id, "myTextureSampler")

    # Read our OBJ file
    vertices,faces,uvs,normals,colors = objloader.load(".\\content\\cube.obj")
    vertex_data,uv_data,normal_data = objloader.process_obj( vertices,faces,uvs,normals,colors)

    # Our OBJ loader uses Python lists, convert to ctype arrays before sending to OpenGL
    vertex_data = objloader.generate_2d_ctypes(vertex_data)
    uv_data = objloader.generate_2d_ctypes(uv_data)

    # Load OBJ in to a VBO
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, len(vertex_data) * 4 * 3, vertex_data, GL_STATIC_DRAW)

    uv_buffer = glGenBuffers(1)
    array_type = GLfloat * len(uv_data)
    glBindBuffer(GL_ARRAY_BUFFER, uv_buffer)
    glBufferData(GL_ARRAY_BUFFER, len(uv_data) * 4 * 2, uv_data, GL_STATIC_DRAW)

    # vsync and glfw do not play nice.  when vsync is enabled mouse movement is jittery.
    common.disable_vsyc()
    
    while glfw.get_key(window,glfw.KEY_ESCAPE) != glfw.PRESS and not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT)

        glUseProgram(program_id)

        controls.computeMatricesFromInputs(window)
        ProjectionMatrix = controls.getProjectionMatrix()
        ViewMatrix = controls.getViewMatrix()
        ModelMatrix = mat4.identity()
        mvp = ProjectionMatrix * ViewMatrix * ModelMatrix

        # Send our transformation to the currently bound shader, 
        # in the "MVP" uniform
        glUniformMatrix4fv(matrix_id, 1, GL_FALSE,mvp.data)
        
        # Bind our texture in Texture Unit 0
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        # Set our "myTextureSampler" sampler to user Texture Unit 0
        glUniform1i(texture_id, 0)

        #1rst attribute buffer : vertices
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
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
        glBindBuffer(GL_ARRAY_BUFFER, uv_buffer)
        glVertexAttribPointer(
            1,                  # attribute 1. No particular reason for 1, but must match the layout in the shader.
            2,                  # len(vertex_data)
            GL_FLOAT,           # type
            GL_FALSE,           # ormalized?
            0,                  # stride
            null                # array buffer offset (c_type == void*)
            )

        # Draw the triangles, vertex data now contains individual vertices
        # so use array length
        glDrawArrays(GL_TRIANGLES, 0, len(vertex_data))

        # Not strictly necessary because we only have 
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
    
    
        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    # !Note braces around vertex_buffer and uv_buffer.  
    # glDeleteBuffers expects a list of buffers to delete
    glDeleteBuffers(1, [vertex_buffer])
    glDeleteBuffers(1, [uv_buffer])
    glDeleteProgram(program_id)
    glDeleteTextures([texture_id])
    glDeleteVertexArrays(1, [vertex_array_id])

    glfw.terminate()

if __name__ == "__main__":
    main()
