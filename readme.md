
# OpenGL-Tutorials in Python

This repository contains Python versions of the C++ tutorials at [opengl-tutorials](www.opengl-tutorials.org).

The Python code was written to be as close to the original C++ code as possible.  Certain concessions were made to accomodate missing libraries and to match Python's style guide wherever possible.  One good example of missing functionality is the [glew](http://glew.sourceforge.net/) library.  The most up to date Python-glew wrapper is almost 10 years old and it does not play nicely with Python 3.x.

Currently only the source code has been converted.  The actual tutorials are not finished but will be coming soon and with the original author's permission.

##Requirements
---
1. Python 3.X [[download](https://www.python.org/download)]
1. PyOpengl && PyOpenGL_Accelerate:  `pip install pyopengl pyopengl_accelerate`
1. Pillow (a Python Image Library (PIL) fork):  `pip install pillow`
1. pyglfw (a glfw wrapper)
  * Download [pyglfw](https://github.com/FlorianRhiem/pyGLFW), unpack, and run `python setup.py install`
  * Download [glfw](http://www.glfw.org/) binaries for your OS.  
    * Linux users:  You should be all set after installation.  
    * Windows users: Copy the **glfw** binaries in the tutorials folder or modify `pyglfw.py` to use Windows paths, by default `pyglfw.py` is set to common Linux paths.

##Replacements
---
A few of the original C++ tutorials contain references to libraries that don't have Python equivalents or the equivalent libraries were beyond the scope of a simple tutorial.  Here is a quick table showing what has been replaced:


CPP Tutorials  |  Python Tutorials
-------------  |  ----------------
glm            |  cgsl
glew           |  glew_wish
obj loader     |  objloader.py


* **cgsl**: Curiously simple graphics library (CSGL) is a hacky little bit of code I threw together to mimic GLM from the original C++ tutorials. Given more time I may go back and do a proper port. The idea with CSGL was to avoid using complex modules like Numpy that are beyond the scope of these tutorials.
* **glew_wish**: Very much a tongue in cheek kludge to support GLEW's function querying.  GLEW is rarely used in the beginner tutorials so this code was never finished.  It will handle the basics and the reason can take it as an exercise to finish what I started or do a proper GLEW port.  In a perfect world I would do something similar to `pyglfw` like wrapping the GLEW binaries.
* **objloader.py**: The original C++ code creates its own Wavefront OBJ loader that supports a very specific output format from Blender.  I copied the original tutorials exactly, meaning you need both  UVs and Normals in your Blender output or `objloader.py` won't know what to do.


## Completed Conversions

* Basic OpenGL
  * Tutorial 1 : Opening a window [[source](https://github.com/Jerdak/opengl_tutorials_python/blob/master/tutorial1.py)]
  * Tutorial 2 : The first triangle [[source](https://github.com/Jerdak/opengl_tutorials_python/blob/master/tutorial2.py)]
  * Tutorial 3 : Matrices [[source](https://github.com/Jerdak/opengl_tutorials_python/blob/master/tutorial3.py)]
  * Tutorial 4 : A Colored Cube [[source](https://github.com/Jerdak/opengl_tutorials_python/blob/master/tutorial4.py)]
  * Tutorial 5 : A Textured Cube [[source](https://github.com/Jerdak/opengl_tutorials_python/blob/master/tutorial5.py)]
  * Tutorial 6 : Keyboard and Mouse [[source](https://github.com/Jerdak/opengl_tutorials_python/blob/master/tutorial6.py)]
  * Tutorial 7 : Model loading [[source](https://github.com/Jerdak/opengl_tutorials_python/blob/master/tutorial7.py)]
  * Tutorial 8 : Basic shading [[source](https://github.com/Jerdak/opengl_tutorials_python/blob/master/tutorial8.py)]
* Intermediate Tutorials
  * Tutorial 9 : VBO Indexing [[source](https://github.com/Jerdak/opengl_tutorials_python/blob/master/tutorial9.py)]
  * Tutorial 10 : Transparency [[source](https://github.com/Jerdak/opengl_tutorials_python/blob/master/tutorial10.py)]

## Ongoing Conversions
  * Tutorial 11 : 2D text
  * Tutorial 12 : OpenGL Extensions
  * Tutorial 13 : Normal Mapping
  * Tutorial 14 : Render To Texture
  * Tutorial 15 : Lightmaps
  * Tutorial 16 : Shadow mapping
  * Tutorial 17 : Rotations
  * Tutorial 18 : Billboards & Particles

# License(s)

### Original
[WTFPL Public License Version 2](http://www.opengl-tutorial.org/download/)*

*Note: The language of WTFPL is unprofessional and will not be restated here.  Initially I released my code under WTFPL but after some deliberation I decided against using WTFPL.

### Current
The MIT License (MIT)

Copyright (c) 2014 Jeremy Carson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
