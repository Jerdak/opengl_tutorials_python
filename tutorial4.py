#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" Tutorial 4: A Colored Cube
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
	window = glfw.create_window(1024, 768, "Tutorial 04", None, None) #(in the accompanying source code this variable will be global)
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


def key_event(window,key,scancode,action,mods):
	""" Handle keyboard events

		Note:  It's not important to understand how this works just yet.
		Keyboard and mouse inputs are covered in Tutorial 6
	"""
	if action == glfw.PRESS and key == glfw.KEY_D:
		if glIsEnabled (GL_DEPTH_TEST): glDisable(GL_DEPTH_TEST)
		else: glEnable(GL_DEPTH_TEST)

		glDepthFunc(GL_LESS)

def main():
	if not opengl_init():
		return

	# Enable key events
	glfw.set_input_mode(window,glfw.STICKY_KEYS,GL_TRUE) 
	
	# Enable key event callback
	glfw.set_key_callback(window,key_event)

	# Set opengl clear color to something other than red (color used by the fragment shader)
	glClearColor(0,0,0.4,0)
	
	vertex_array_id = glGenVertexArrays(1)
	glBindVertexArray( vertex_array_id )

	program_id = common.LoadShaders( ".\\shaders\\Tutorial4\\TransformVertexShader.vertexshader",
		".\\shaders\\Tutorial4\\ColorFragmentShader.fragmentshader" )
	
	# Get a handle for our "MVP" uniform
	matrix_id= glGetUniformLocation(program_id, "MVP");

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

	# One color for each vertex. They were generated randomly.
	color_data = [ 
		0.583,  0.771,  0.014,
		0.609,  0.115,  0.436,
		0.327,  0.483,  0.844,
		0.822,  0.569,  0.201,
		0.435,  0.602,  0.223,
		0.310,  0.747,  0.185,
		0.597,  0.770,  0.761,
		0.559,  0.436,  0.730,
		0.359,  0.583,  0.152,
		0.483,  0.596,  0.789,
		0.559,  0.861,  0.639,
		0.195,  0.548,  0.859,
		0.014,  0.184,  0.576,
		0.771,  0.328,  0.970,
		0.406,  0.615,  0.116,
		0.676,  0.977,  0.133,
		0.971,  0.572,  0.833,
		0.140,  0.616,  0.489,
		0.997,  0.513,  0.064,
		0.945,  0.719,  0.592,
		0.543,  0.021,  0.978,
		0.279,  0.317,  0.505,
		0.167,  0.620,  0.077,
		0.347,  0.857,  0.137,
		0.055,  0.953,  0.042,
		0.714,  0.505,  0.345,
		0.783,  0.290,  0.734,
		0.722,  0.645,  0.174,
		0.302,  0.455,  0.848,
		0.225,  0.587,  0.040,
		0.517,  0.713,  0.338,
		0.053,  0.959,  0.120,
		0.393,  0.621,  0.362,
		0.673,  0.211,  0.457,
		0.820,  0.883,  0.371,
		0.982,  0.099,  0.879]

	vertex_buffer = glGenBuffers(1);
	array_type = GLfloat * len(vertex_data)
	glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
	glBufferData(GL_ARRAY_BUFFER, len(vertex_data) * 4, array_type(*vertex_data), GL_STATIC_DRAW)

	color_buffer = glGenBuffers(1);
	array_type = GLfloat * len(color_data)
	glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
	glBufferData(GL_ARRAY_BUFFER, len(color_data) * 4, array_type(*color_data), GL_STATIC_DRAW)



	while glfw.get_key(window,glfw.KEY_ESCAPE) != glfw.PRESS and not glfw.window_should_close(window):
		glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT)

		glUseProgram(program_id)

		# Send our transformation to the currently bound shader, 
		# in the "MVP" uniform
		glUniformMatrix4fv(matrix_id, 1, GL_FALSE,mvp.data)
		# Bind vertex buffer data to the attribute 0 in our shader.
		# Note:  This can also be done in the VAO itself (see vao_test.py)

		# Enable the vertex attribute at element[0], in this case that's the triangle's vertices
		# this could also be color, normals, etc.  It isn't necessary to disable these
		#
		#1rst attribute buffer : vertices
		glEnableVertexAttribArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer);
		glVertexAttribPointer(
			0,                  # attribute 0. No particular reason for 0, but must match the layout in the shader.
			3,                  # len(vertex_data)
			GL_FLOAT,           # type
			GL_FALSE,           # ormalized?
			0,                  # stride
			null           		# array buffer offset (c_type == void*)
			)

		# 2nd attribute buffer : colors
		glEnableVertexAttribArray(1)
		glBindBuffer(GL_ARRAY_BUFFER, color_buffer);
		glVertexAttribPointer(
			1,                  # attribute 0. No particular reason for 0, but must match the layout in the shader.
			3,                  # len(vertex_data)
			GL_FLOAT,           # type
			GL_FALSE,           # ormalized?
			0,                  # stride
			null           		# array buffer offset (c_type == void*)
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
	glDeleteBuffers(1, [color_buffer])
	glDeleteProgram(program_id)
	glDeleteVertexArrays(1, [vertex_array_id])

	glfw.terminate()

if __name__ == "__main__":
	main()
