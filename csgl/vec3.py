#! /usr/bin/env python
""" The curiously simply graphics library

	A quick stand-in for the OpenGL mathematics (GLM) library.
	PyOpenGL supports numpy 
"""
from OpenGL.GL import *
from multimethods import multimethod
from multimethods import multimethod2

import sys
import math
import copy
import operator

def arith(op,a,b):
	btype = type(b)
	if btype is vec3:
		return vec3(op(a.x,b.x),op(a.y,b.y),op(a.z,b.z))
	elif btype is float or btype is int:
		return vec3(op(a.x,b),op(a.y,b),op(a.z,b))

class vec3(object):
	def __init__(self,x=0,y=0,z=0):
		self.data_ = (GLfloat * 3)()
		self.x = x
		self.y = y
		self.z = z
	
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


	def length(self):
		return math.sqrt(self.sqr_length())

	def sqr_length(self):
		return self.x*self.x + self.y*self.y + self.z*self.z

	@staticmethod
	def lerp(a,b,t):
		ba = b-a
		return a + t*(ba)

	@staticmethod
	def cross(a,b):
		return vec3(a.y*b.z-a.z*b.y,a.z*b.x-a.x*b.z,a.x*b.y-a.y*b.x)

	@staticmethod
	def dot(a,b):
		return a.x*b.x + a.y*b.y + a.z*b.z
	
	def normalize(self):
		l = self.length()
		self.x = self.x / l
		self.y = self.y / l
		self.w = self.z / l

	def normalized(self):
		l = self.length()
		return vec3(self.x / l, self.y / l, self.z / l)
	
	@staticmethod
	def arith(op,a,b):
		rtype = type(b)
		if rtype is vec3:
			return vec3(op(a.x,b.x),op(a.y,b.y),op(a.z,b.z))
		elif rtype is float or rtype is int:
			return vec3(op(a.x,b),op(a.y,b),op(a.z,b))

	@staticmethod
	def arith_inline(op,a,b):
		rtype = type(b)
		if rtype is vec3:
			a.x = op(a.x,b.x)
			a.y = op(a.y,b.y)
			a.z = op(a.z,b.z)
			return a
		elif rtype is float or rtype is int:
			a.x = op(a.x,b)
			a.y = op(a.y,b)
			a.z = op(a.z,b)
			return a

	def __add__(self, other):return vec3.arith(operator.add,self,other)
	def __iadd__(self,other):return vec3.arith_inline(operator.add,self,other)
	def __radd__(self,other):return vec3.arith(operator.add,self,other)
	
	def __sub__(self, other):return vec3.arith(operator.sub,self,other)
	def __isub__(self,other):return vec3.arith_inline(operator.sub,self,other)
	def __rsub__(self,other):return vec3.arith(operator.sub,self,other)

	def __mul__(self, other):return vec3.arith(operator.mul,self,other)
	def __imul__(self,other):return vec3.arith_inline(operator.mul,self,other)
	def __rmul__(self,other):return vec3.arith(operator.mul,self,other)

	def __div__(self, other):return vec3.arith(operator.div,self,other)
	def __idiv__(self,other):return vec3.arith_inline(operator.div,self,other)
	def __rdiv__(self,other):return vec3.arith(operator.div,self,other)

	def __eq__(self,other):
		if math.fabs(self.x - other.x) >= sys.float_info.epsilon:return False
		if math.fabs(self.y - other.y) >= sys.float_info.epsilon:return False
		if math.fabs(self.z - other.z) >= sys.float_info.epsilon:return False
		return True

	def __ne__(self,other):
		return not (self==other)

	def __str__(self):
		return unicode(self).encode('utf-8')

	def __unicode__(self):
		return "%f %f %f"%(self.x,self.y,self.z)

def main():
	x = vec3(1,2,3)
	y = vec3(1,2,3)
	xy = x+y
	print(xy)
	print(x+1)
	print(12+x)

	xy = x*y
	print(xy)
	xy = 1+x*y
	print(xy)
	return
	
	xy_actual = vec3(2,4,6)
	assert(xy == xy_actual)

	x = vec3(2,1,-1)
	y = vec3(-3,4,1)
	assert(vec3.cross(x,y)==vec3(5,1,11))
	assert(vec3.cross(y,x)==vec3(-5,-1,-11))

	vec3.lerp(x,y,0.5)
if __name__=='__main__':
	main()
