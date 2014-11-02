
# OpenGL-Tutorials in Python
---

This repository contains Pythons versions of C++ tutorials at [OpenGL-Tutorials.org](www.opengl-tutorials.org).

For the most part the Python code mimics the original C++ code with a few tweaks to accomodate missing libraries.  For instance, at the time of this writing the Python [glew](http://glew.sourceforge.net/) wrapper was almost 10 years old and it did not play well with Python 3.4.

Python-specific tutorials are coming soon (w/ original author's permission).

##License(s)
---
The original source was released under WTFPL Public License, my Python version of that code is released under WTFPL Public Licence as well.

##Requirements
---
1. Python 3.X [[download](https://www.python.org/download)]
1. PyOpengl && PyOpenGL_Accelerate:  `pip install pyopengl pyopengl_accelerate`
1. Pillow (a Python Image Library (PIL) fork):  `pip install pillow`
1. pyglfw (a glfw wrapper)
  * Download [pyglfw](https://github.com/FlorianRhiem/pyGLFW), unpack, and run `python setup.py install`
  * Download [glfw](http://www.glfw.org/) binaries for your OS.  Linux users should be all set after installation.  Windows users: place the **glfw** binaries in the tutorials folder or modify `pyglfw.py` to use Windows paths, by default `pyglfw.py` is geared to Linux users.

##Replacements
---
A few of the original C++ tutorials contain references to libraries that don't have Python equivalents or the equivalent libraries were beyond the scope of a simple tutorial.  Here is a quick table showing what has been replaced:


CPP Tutorials  |  Python Tutorials
-------------  |  ----------------
glm            |  cgsl 
glew           |  glew_wish
obj loader     |  objloader.py


* **cgsl**: Curiously simple graphics library (CSGL) is a hacky little bit of code I threw together to mimic GLM in the original C++ tutorials. Given more time I may go back and do a proper port. The idea with CSGL was to avoid using complex modules like Numpy that are beyond the scope of these tutorials. The reader has enough mental bandwidth issues without also having to understand Numpy's mechanics.
* **glew_wish**: Very much a tongue in cheek kludge to support GLEW's functionality querying.  GLEW is rarely used in the beginner tutorials so this code is unfinished.
* **objloader.py**: The original C++ code creates its own Wavefront OBJ loader that supports a very specific output format from Blender.  I copied the original tutorials exactly meaning you need both a UVs and Normals or the importer won't know what to do.
 

##Completed Conversions

* Basic OpenGL
  * Tutorial 1 : Opening a window [[source](https://github.com/Jerdak/opengl_tutorials_python/blob/master/tutorial1.py)]
  * Tutorial 2 : The first triangle [[source](https://github.com/Jerdak/opengl_tutorials_python/blob/master/tutorial2.py)]
  * Tutorial 3 : Matrices [[source](https://github.com/Jerdak/opengl_tutorials_python/blob/master/tutorial3.py)]
  * Tutorial 4 : A Colored Cube [[source](https://github.com/Jerdak/opengl_tutorials_python/blob/master/tutorial4.py)]
  * Tutorial 5 : A Textured Cube [[source](https://github.com/Jerdak/opengl_tutorials_python/blob/master/tutorial5.py)]
  * Tutorial 6 : Keyboard and Mouse [[source](https://github.com/Jerdak/opengl_tutorials_python/blob/master/tutorial6.py)]
  * Tutorial 7 : Model loading [[source](https://github.com/Jerdak/opengl_tutorials_python/blob/master/tutorial7.py)]
  * Tutorial 8 : Basic shading [[source](https://github.com/Jerdak/opengl_tutorials_python/blob/master/tutorial8.py)]

##Ongoing Conversions
* Intermediate Tutorials
  * Tutorial 9 : VBO Indexing [[source](https://github.com/Jerdak/opengl_tutorials_python/blob/master/tutorial9.py)]
  * Tutorial 10 : Transparency
  * Tutorial 11 : 2D text
  * Tutorial 12 : OpenGL Extensions
  * Tutorial 13 : Normal Mapping
  * Tutorial 14 : Render To Texture
  * Tutorial 15 : Lightmaps
  * Tutorial 16 : Shadow mapping
  * Tutorial 17 : Rotations
  * Tutorial 18 : Billboards & Particles
