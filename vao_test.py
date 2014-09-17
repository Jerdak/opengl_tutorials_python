#! /usr/bin/env python
""" Tutorial 2: Drawing the triangle
"""

from __future__ import print_function

from OpenGL.GL import *
from OpenGL.GL.ARB import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.special import *
from OpenGL.GL.shaders import *

from test import *
from glew_wish import *
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
	window = glfw.create_window(1024, 768, "VAO Test", None, None) #(in the accompanying source code this variable will be global)
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


	# !!NOTE: The most recent GLEW package for python is 8 years old, ARB functionality
	# is available in Pyopengl natively.

	if glewInit() != GLEW_OK:
	 	print("Failed to initialize GLEW\n",file=sys.stderr);
	 	return False
	return True


current_vao = 0
vaos = []
def key_event(window,key,scancode,action,mods):
	global current_vao
	if action == glfw.PRESS and key == glfw.KEY_W:
		current_vao+=1
		current_vao = current_vao % len(vaos)


def init_object(vertices):
	array_type = GLfloat * len(vertex_data)

	glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
	glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, array_type(*vertices), GL_STATIC_DRAW)

	glEnableVertexAttribArray(0)
	glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,null)
	

vertex_data = [-1.0, -1.0, 0.0,
				1.0, -1.0, 0.0,
				0.0,  1.0, 0.0]

vertex_data2 = [0.0, -1.0, 0.0,
				1.0, -1.0, 0.0,
				0.0,  1.0, 0.0]


def main():
	global current_vao
	global vaos

	if not opengl_init():
		return

	glfw.set_input_mode(window,glfw.STICKY_KEYS,GL_TRUE) 
	glfw.set_key_callback(window,key_event)
	# Set opengl clear color to something other than red (color used by the fragment shader)
	glClearColor(0,0,0.4,0)
	
	# Create vertex array object (VAO) 1: Full Triangle
	vao = glGenVertexArrays(1)
	glBindVertexArray(vao)
	init_object(vertex_data)
	glBindVertexArray(0)

	# Create vertex array object (VAO) 2: 1/2 Triangle
	vao2 = glGenVertexArrays(1)
	glBindVertexArray(vao2)
	init_object(vertex_data2)
	glBindVertexArray(0)

	program_id = common.LoadShaders( "SimpleVertexShader.vertexshader", "SimpleFragmentShader.fragmentshader" )
	vertex_buffer = glGenBuffers(1)

	current_vao = 0
	vaos = [vao,vao2]
	glewInit()


	while glfw.get_key(window,glfw.KEY_ESCAPE) != glfw.PRESS and not glfw.window_should_close(window):
		glClear(GL_COLOR_BUFFER_BIT)

		glUseProgram(program_id)	
		glBindVertexArray(vaos[current_vao])

		# Draw the triangle !
		glDrawArrays (GL_TRIANGLES, 0, 3)#3 indices starting at 0 -> 1 triangle

		glBindVertexArray(0)

		# Swap front and back buffers
		glfw.swap_buffers(window)

		# Poll for and process events
		glfw.poll_events()

	glfw.terminate()

if __name__ == "__main__":
	main()
