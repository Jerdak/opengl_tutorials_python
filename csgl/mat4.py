#! /usr/bin/env python
""" The curiously simply graphics library

	A quick stand-in for the OpenGL mathematics (GLM) library.
	PyOpenGL supports numpy 
"""

from __future__ import print_function
from OpenGL.GL import *
from vec3 import *
from ctypes import *

import sys
import math
import copy

class mat4(object):
	def __init__(self,*data):
		self.data_ = (GLfloat * 16)()
		if len(data) == 16:
			for i,d in enumerate(data): self.data_[i] = data[i]
		if len(data) == 1:
			for i,d in enumerate(data[0]): self.data_[i] = data[0][i]
		#if len(data) == 4:

	def copy(self):
		return copy.deepcopy(self)

	# [Xx Yx Zx Tx]  [0 4 8  12]
	# [Xy Yy Zy Ty]  [1 5 9  13]
	# [Xz Yz Zz Tz]  [2 6 10 14]
	# [0  0  0  1 ]  [3 7 11 15]

	def __getitem__(self,r):
		return pointer(GLfloat.from_address(addressof(self.data_) + sizeof(GLfloat) * r* 4))

	@staticmethod
	def zeroes():
		return mat4.fill(0)

	@staticmethod
	def fill(v):
		return mat4([v for i in range(0,16)])

	@staticmethod
	def identity():
		return mat4(
			1,0,0,0,
			0,1,0,0,
			0,0,1,0,
			0,0,0,1)

	@staticmethod
	def perspective(fov_deg,aspect,z_near,z_far):
		assert(aspect != 0.0)
		assert(z_near != z_far)

		fov = math.radians(fov_deg)
		tan_half_fov = math.tan(fov / 2.0)

		m = mat4.zeroes()
		m[0][0] = 1.0 / (aspect * tan_half_fov)
		m[1][1] = 1.0 / (tan_half_fov)
		m[2][2] = -(z_far+z_near) / (z_far - z_near)
		m[2][3] = -1.0
		m[3][2] = -(2.0 * z_far * z_near) / (z_far - z_near) 
		return m

	@staticmethod
	def lookat(eye,center,up):
		f = (center-eye).normalized()
		s = (vec3.cross(f,up).normalized())
		u = (vec3.cross(s,f))

		m = mat4.identity()
		m[0][0] = s.x
		m[1][0] = s.y
		m[2][0] = s.z

		m[0][1] = u.x;
		m[1][1] = u.y;
		m[2][1] = u.z;

		m[0][2] =-f.x;
		m[1][2] =-f.y;
		m[2][2] =-f.z;

		m[3][0] =-vec3.dot(s, eye);
		m[3][1] =-vec3.dot(u, eye);
		m[3][2] = vec3.dot(f, eye);
		return m

	def rotatex(self,angle):
		rad = math.radians(angle)
		m = self
		m[0][2] = math.cos(rad)
		m[0][3] = math.sin(rad)
		m[2][0] = -math.sin(rad)
		m[2][2] = math.cos(rad)

	def translate(self,vec3):
		self.data_[12] = vec3.x
		self.data_[13] = vec3.y
		self.data_[14] = vec3.z

	def __add__(self,other):
		data = [self.data_[i] + other.data_[i] for i in range(0,16)] 
		return mat4(*data)
	
	def __iadd__(self,other):
		self.x += other.x
		self.y += other.y
		self.z += other.z
		return self

	def __mul__(self,other):
		m = mat4.zeroes()
		a = other#self
		b = self#other
		
		for r in range(0,4):
			for c in range(0,4):
				for i in range(0,4):
					m[r][c] += a[r][i] * b[i][c]

		print("result--\n",m)
		return m
	
	#def __imul__(self,other):
	#	self.x *= other.x
	#	self.y *= other.y
#		self.z *= other.z
#		return self

	# def __sub__(self,other):
	# 	return vec3(self.x-other.x,self.y-other.y,self.z-other.z)
	
	# def __isub__(self,other):
	# 	self.x -= other.x
	# 	self.y -= other.y
	# 	self.z -= other.z
	# 	return self

	# def __sub__(self,other):
	# 	return vec3(self.x-other.x,self.y-other.y,self.z-other.z)
	
	# def __isub__(self,other):
	# 	self.x -= other.x
	# 	self.y -= other.y
	# 	self.z -= other.z
	# 	return self

	# def __mul__(self,other):
	# 	return vec3(self.x*other.x,self.y*other.y,self.z*other.z)
	
	# def __imul__(self,other):
	# 	self.x *= other.x
	# 	self.y *= other.y
	# 	self.z *= other.z
	# 	return self


	# def __div__(self,other):
	# 	return vec3(self.x/other.x,self.y/other.y,self.z/other.z)
	
	# def __idiv__(self,other):
	# 	self.x /= other.x
	# 	self.y /= other.y
	# 	self.z /= other.z
	# 	return self

	# def __eq__(self,other):
	# 	if math.fabs(self.x - other.x) >= sys.float_info.epsilon:return False
	# 	if math.fabs(self.y - other.y) >= sys.float_info.epsilon:return False
	# 	if math.fabs(self.z - other.z) >= sys.float_info.epsilon:return False
	# 	return True

	# def __ne__(self,other):
	# 	return not (self==other)


	def __str__(self):
		return unicode(self).encode('utf-8')

	def __unicode__(self):
		return "%f %f %f %f\n%f %f %f %f\n%f %f %f %f\n%f %f %f %f\n"%(
			self.data_[0],self.data_[1],self.data_[2],self.data_[3],
			self.data_[4],self.data_[5],self.data_[6],self.data_[7],
			self.data_[8],self.data_[9],self.data_[10],self.data_[11],
			self.data_[12],self.data_[13],self.data_[14],self.data_[15]
		)
#vec3 constants
# vec3.zero = vec3(0,0,0)
# vec3.up = vec3(0,1,0)
# vec3.down = vec3(0,-1,0)
# vec3.right = vec3(1,0,0)
# vec3.left = vec3(-1,0,0)
# vec3.forward = vec3(0,0,-1)
# vec3.backward = vec3(0,0,1)

def main():
	x = mat4(
		1,1,1,1,
		1,1,1,1,
		1,1,1,1,
		1,1,1,1)
	y = mat4(
		1,1,1,1,
		1,1,1,1,
		1,1,1,1,
		1,1,1,1)

	xpy = x+y
	print(x)
	print(xpy)

	arr = c_int * 5
	x = arr(0,1,2,3,4)
	y = pointer(c_int.from_address(addressof(x) + sizeof(c_int)))
	print(y[1])
	projection = mat4.perspective(45.0, 4.0 / 3.0, 0.1, 100.0)
	view = mat4.lookat(vec3(4,3,3), # Camera is at (4,3,3), in World Space
					vec3(0,0,0), # and looks at the origin
					vec3(0,1,0)) 
	model = mat4.identity()

	mvp = model * view * projection

	print(mvp)
	x = mat4.zeroes()
	x[0][0] = 1
	x[1][0] = 1
	x[2][0] = 1
	x[0][1] = 2
	x[1][1] = 2
	x[2][1] = 2
	x[0][2] = 3
	x[1][2] = 3
	x[2][2] = 3
	x[3][0] = 4
	x[3][1] = 4
	x[3][2] = 4
	print(x)
	#glm::mat4 MVP        = Projection * View * Model;
#	mvp = 
	#x[0][4]
if __name__=='__main__':
	main()
