#! /usr/bin/env python
from __future__ import print_function

from csgl.vec3 import *
from csgl.vec4 import *
from csgl.mat4 import *

import unittest
import random
import os
import sys



class Testvec4Operators(unittest.TestCase):
    def setUp(self):
        # hardcode seed to keep results identical
        random.seed(42) 

        # Python "float" is implemented as C++ double
        self._data_x = [random.randint(0,100) for i in range(0,4)]
        self._data_y = [random.randint(0,100) for i in range(0,4)]
        self._data_scalar = random.randint(0,100)                


    def test_addition(self):
        a = vec4(*self._data_x)
        b = vec4(*self._data_y)
        c = self._data_scalar

        ab = a+b
        self.assertEqual(ab.x,a.x+b.x)
        self.assertEqual(ab.y,a.y+b.y)
        self.assertEqual(ab.z,a.z+b.z)   
        self.assertEqual(ab.w,a.w+b.w)        

        ac = a + c
        self.assertAlmostEqual(ac.x,a.x+c,places=6)
        self.assertAlmostEqual(ac.y,a.y+c,places=6)
        self.assertAlmostEqual(ac.z,a.z+c,places=6)
        self.assertAlmostEqual(ac.w,a.w+c,places=6)

    def test_subtraction(self):
        a = vec4(*self._data_x)
        b = vec4(*self._data_y)
        c = self._data_scalar

        ab = a-b
        self.assertEqual(ab.x,a.x-b.x)
        self.assertEqual(ab.y,a.y-b.y)
        self.assertEqual(ab.z,a.z-b.z)
        self.assertEqual(ab.w,a.w-b.w)

        ac = a - c
        self.assertAlmostEqual(ac.x,a.x-c,places=6)
        self.assertAlmostEqual(ac.y,a.y-c,places=6)
        self.assertAlmostEqual(ac.z,a.z-c,places=6)
        self.assertAlmostEqual(ac.w,a.w-c,places=6)

    def test_division(self):
        a = vec4(*self._data_x)
        b = vec4(*self._data_y)

        # avoid div by 0
        a.w = a.w if a.w != 0.0 else random.randint(1,100)
        b.w = b.w if a.w != 0.0 else random.randint(1,100)
        c = self._data_scalar if self._data_scalar != 0 else random.randint(1,100)

        ab = a/b
        self.assertAlmostEqual(ab.x,a.x/b.x,places=6)
        self.assertAlmostEqual(ab.y,a.y/b.y,places=6)
        self.assertAlmostEqual(ab.z,a.z/b.z,places=6)
        self.assertAlmostEqual(ab.w,a.w/b.w,places=6)

        ac = a / c
        self.assertAlmostEqual(ac.x,a.x/c,places=6)
        self.assertAlmostEqual(ac.y,a.y/c,places=6)
        self.assertAlmostEqual(ac.z,a.z/c,places=6)
        self.assertAlmostEqual(ac.w,a.w/c,places=6)

    def test_multiplication(self):
        a = vec4(*self._data_x)
        b = vec4(*self._data_y)
        c = self._data_scalar

        ab = a*b
        self.assertAlmostEqual(ab.x,a.x*b.x,places=6)
        self.assertAlmostEqual(ab.y,a.y*b.y,places=6)
        self.assertAlmostEqual(ab.z,a.z*b.z,places=6)
        self.assertAlmostEqual(ab.w,a.w*b.w,places=6)

        ac = a * c
        self.assertAlmostEqual(ac.x,a.x*c,places=6)
        self.assertAlmostEqual(ac.y,a.y*c,places=6)
        self.assertAlmostEqual(ac.z,a.z*c,places=6)
        self.assertAlmostEqual(ac.w,a.w*c,places=6)

def main():
    unittest.main()


if __name__=='__main__':
    main()