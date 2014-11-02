#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" Tutorial 1: Opening a Window
"""

from __future__ import print_function

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.special import *
from OpenGL.GL.shaders import *

from glew_wish import *
import glfw
import sys
import os

def main():
    # Initialize the library
	if not glfw.init():
		return

	# Open Window and create its OpenGL context
	window = glfw.create_window(1024, 768, "Tutorial 01", None, None)

	# 
	glfw.window_hint(glfw.SAMPLES, 4)
	glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
	glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
	glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
	glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
 
	if not window:
		print("Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible. Try the 2.1 version of the tutorials.\n",file=sys.stderr)
		glfw.terminate()
		return

	# Initialize GLEW
	glfw.make_context_current(window)
	glewExperimental = True

	# GLEW is a framework for testing extension availability.  Please see tutorial notes for
	# more information including why can remove this code.
	if glewInit() != GLEW_OK:
	 	print("Failed to initialize GLEW\n",file=sys.stderr);
	 	return
	
	glfw.set_input_mode(window,glfw.STICKY_KEYS,True) 


	# Loop until the user closes the window
	
	#while not glfw.window_should_close(window):
	while glfw.get_key(window,glfw.KEY_ESCAPE) != glfw.PRESS and not glfw.window_should_close(window):

		# Draw nothing sucker

		# Swap front and back buffers
		glfw.swap_buffers(window)

		# Poll for and process events
		glfw.poll_events()

	glfw.terminate()

if __name__ == "__main__":
	main()

