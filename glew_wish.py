#! /usr/bin/env python
""" Temporary stand-in for GLEW functionality until a proper Python
	module is created

	glew_wish = you wish... get it.  Oh my god I'm so funny.

	The naming convention in this script mimics that of the 
	official GLEW API, that should make switching to the real
	thing a little easier.

	TODO:
		[] -  See http://pyopengl.sourceforge.net/documentation/opengl_diffs.html and consider scrapping the GLEW
    lookup or simply wrapping PyOpenGL's native behaviour.
"""
from __future__ import print_function

from OpenGL.GL import *
from OpenGL.GL.ARB import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.special import *
from OpenGL.GL.shaders import *
from OpenGL.extensions import *

import collections
import re
import glfw

GLEW_INITIALIZED = False
GLEW_ERR = 0
GLEW_OK = 1
GLEW_OGL_INFO = None
GL_VERSIONS = "GL_VERSION"

def glewAreYouKidding():
	""" Ugly ugly ugly hack to push GLEW variables in to the global namespace

		The GLEW header contains macros and definitions to enumerate
		available OpenGL functionality. The only way to provide these
		variables in the global namespace of Python is to
		work backwards through the call stack to add them globally
        to each calling stack frame.


		Note:  Seriously, this is a garbage hack.  It will *heavily* pollutes
        all calling namespaces.

        Some functionality here might be useful later for injecting GLEW-like
        definitions in to Python.  Alternatively these functions could just 
        be moved in to a class that adds them to its members

	"""
	if not GLEW_INITIALIZED:
		print("GLEW not initialized, call glewInit() first",file=stderr)
		return

	import inspect

	this_frame = inspect.currentframe()
	stack_frames = set()

	# ignore *this* object
	for s in inspect.stack():
		if s[0] != this_frame:
			stack_frames.add(s[0])

def glewIsSupported(var):
	""" Return True if var is valid extension/core pair

		Usage: glewIsSupported("GL_VERSION_1_4  GL_ARB_point_sprite")

		Note:  GLEW API was not well documented and this function was
		written in haste so the actual GLEW format for glewIsSupported
		might be different.

		TODO: 
			- Only the extension parameter is currently checked. Validate
			the core as well.  Will likely require scraping opengl docs
			for supported functionality
	"""
	var = re.sub(' +',' ',var)
	variables = var.split(' ')
	for v in variables:
		#if v in GLEW_OGL_INFO[GL_VERSIONS]:
		#	return True
		if v in GLEW_OGL_INFO[GL_EXTENSIONS]:
			return True
	return False

def glewGetExtension(extension):
	""" Return True if valid extension
	"""
	if extension in GLEW_OGL_INFO[GL_EXTENSIONS]:
		return True
	return False

def glewInit(unsafe=False):
	""" GLEW initialization hack

        Glew Python packages are severely stale.  PyOpenGL does a 
        good job of exposing available functionality for OpenGL.
        It's likely GLEW is part of the PyOpenGL source (TODO: verify)
		
        This glewInit works and will actually come up with a set of valid
        extensions supported by user's graphics card.

		Input
			unsafe (bool): if true, calls glewAreYouKidding to add glew definitions
			to Pythons call stack (every single file)
	"""
	global GLEW_OK
	global GLEW_INITIALIZED
	global GLEW_OGL_INFO

	GLEW_OGL_INFO = collections.defaultdict(list)
	for name in (GL_VENDOR,GL_RENDERER,GL_VERSION,GL_SHADING_LANGUAGE_VERSION,GL_EXTENSIONS):
		GLEW_OGL_INFO[name] = glGetString(name).decode().split(' ')
		
	#It might be necessariy to use glGetStringi for extensions, so far glGetString has worked
	#GLEW_OGL_INFO[GL_EXTENSIONS] = glGetStringi(GL_EXTENSIONS,<index>)
	
	# unique-ify extensions in set making the 'in' operator
	# O(1) average case.
	GLEW_OGL_INFO[GL_EXTENSIONS] = set(GLEW_OGL_INFO[GL_EXTENSIONS])

	# opengl versions as of 2014
	ogl_version_history = {
		1:[1,2,3,4,5],
		2:[0,1],
		3:[0,1,2,3],
		4:[0,1,2,3,4,5]
	}	

	# Extract supported versions using *this* mnachine's graphics settings
	# to infer backwards compatibility (not necessarily true but good for a placeholder)
	GLEW_OGL_INFO[GL_VERSIONS] = set()
	this_major = int(GLEW_OGL_INFO[GL_VERSION][0].split('.')[0])
	this_minor = int(GLEW_OGL_INFO[GL_VERSION][0].split('.')[1])

	for major in range(1,this_major+1):
		for minor in ogl_version_history[major]:
			if major == this_major and minor <= this_minor:
				GLEW_OGL_INFO[GL_VERSIONS].add("GL_VERSION_%d_%d"%(major,minor))
			elif major != this_major:
				GLEW_OGL_INFO[GL_VERSIONS].add("GL_VERSION_%d_%d"%(major,minor))

	GLEW_INITIALIZED = True

	if unsafe:
		glewAreYouKidding()

	return GLEW_OK

def opengl_init():
	global window
	# Initialize the library
	if not glfw.init():
		print("Failed to initialize GLFW\n",file=sys.stderr)
		return False

	# Open Window and create its OpenGL context
	window = glfw.create_window(1024, 768, "Tutorial 02", None, None) #(in the accompanying source code this variable will be global)
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

def main():
	opengl_init()
	glewInit()
	print(GLEW_OGL_INFO[GL_EXTENSIONS])
	print(AVAILABLE_GLU_EXTENSIONS)

if __name__=='__main__':
	main()
