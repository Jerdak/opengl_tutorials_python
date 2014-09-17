#! /usr/bin/env python
""" The curiously simply graphics library

	A quick stand-in for the OpenGL mathematics (GLM) library.
	PyOpenGL supports numpy 
"""
from OpenGL.GL import *

import sys
import math
import copy

class vec4(object):
	def __init__(self,x=0,y=0,z=0,w=0):
		self.data_ = (GLfloat * 4)()
		self.x = x
		self.y = y
		self.z = z
		self.w = w
	
	def copy(self):
		return copy.deepcopy(self)

	@property
	def x(self):
		return self.data_[0]
	@x.setter
	def x(self,value):
		self.data_[0] = value

	@property
	def y(self):
		return self.data_[1]
	@y.setter
	def y(self,value):
		self.data_[1] = value
	
	@property
	def z(self):
		return self.data_[2]
	@z.setter
	def z(self,value):
		self.data_[2] = value
	
	@property
	def w(self):
		return self.data_[3]
	@w.setter
	def w(self,value):
		self.data_[3] = value
	

	def __add__(self,other):
		return vec4(self.x+other.x,self.y+other.y,self.z+other.z,self.w+other.w)
	
	def __iadd__(self,other):
		self.x += other.x
		self.y += other.y
		self.z += other.z
		self.w += other.w
		return self

	def __sub__(self,other):
		return vec4(self.x-other.x,self.y-other.y,self.z-other.z,self.w-other.w)
	
	def __isub__(self,other):
		self.x -= other.x
		self.y -= other.y
		self.z -= other.z
		self.w -= other.w
		return self

	def __sub__(self,other):
		return vec4(self.x-other.x,self.y-other.y,self.z-other.z,self.w-other.w)
	
	def __isub__(self,other):
		self.x -= other.x
		self.y -= other.y
		self.z -= other.z
		self.w -= other.w
		return self

	def __mul__(self,other):
		return vec4(self.x*other.x,self.y*other.y,self.z*other.z,self.w*other.w)
	
	def __imul__(self,other):
		self.x *= other.x
		self.y *= other.y
		self.z *= other.z
		self.w *= other.w
		return self


	def __div__(self,other):
		return vec4(self.x/other.x,self.y/other.y,self.z/other.z,self.w/other.w)
	
	def __idiv__(self,other):
		self.x /= other.x
		self.y /= other.y
		self.z /= other.z
		self.w /= other.w
		return self

	def __eq__(self,other):
		if math.fabs(self.x - other.x) >= sys.float_info.epsilon:return False
		if math.fabs(self.y - other.y) >= sys.float_info.epsilon:return False
		if math.fabs(self.z - other.z) >= sys.float_info.epsilon:return False
		if math.fabs(self.w - other.w) >= sys.float_info.epsilon:return False
		return True

	def __ne__(self,other):
		return not (self==other)

	def __str__(self):
		return unicode(self).encode('utf-8')

	def __unicode__(self):
		return "%f %f %f %f"%(self.x,self.y,self.z,self.w)

#vec4 constants
vec4.zero = vec4(0,0,0,0)
vec4.up = vec4(0,1,0,0)
vec4.down = vec4(0,-1,0,0)
vec4.right = vec4(1,0,0,0)
vec4.left = vec4(-1,0,0,0)
vec4.forward = vec4(0,0,-1,0)
vec4.backward = vec4(0,0,1,0)

def main():
	x = vec4(1,2,3,4)
	y = vec4(1,2,3,4)
	xy = x+y
	xy_actual = vec4(2,4,6,8)

	print(xy == xy_actual)
	assert(xy == xy_actual)
	y = x.copy()
	y.x = 12
	y = vec4.zero
	print x
	print y
	print xy

if __name__=='__main__':
	main()
