#! /usr/bin/env python
from __future__ import print_function

import unittest
import random
import os
import sys

from csgl.vec3 import *
from csgl.vec4 import *
from csgl.mat4 import *

class TestMat4Operators(unittest.TestCase):
    def setUp(self):
        # hardcode seed to keep results identical
        random.seed(42) 

        # Python "float" is implemented as C++ double
        self._data_x = [random.randint(0,100) for i in range(0,16)]
        self._data_y = [random.randint(0,100) for i in range(0,16)]
                


    def test_addition(self):
        x = mat4(*self._data_x)
        y = mat4(*self._data_y)
        xy = x+y

        idx = lambda r,c: r*4 + c

        for r in range(0,4):
            for c in range(0,4):
                self.assertEqual(xy[r][c],self._data_x[idx(r,c)] + self._data_y[idx(r,c)])

    def test_subtraction(self):
        x = mat4(*self._data_x)
        y = mat4(*self._data_y)
        xy = x-y

        idx = lambda r,c: r*4 + c

        for r in range(0,4):
            for c in range(0,4):
                self.assertEqual(xy[r][c],self._data_x[idx(r,c)] - self._data_y[idx(r,c)])

    def test_multiplication(self):
        x = mat4(*self._data_x)
        y = mat4(*self._data_y)
        xy = x*y

        idx = lambda r,c: r*4 + c

        data = [0] * 16
        for r in range(0,4):
            for c in range(0,4):
                for i in range(0,4):
                    data[idx(r,c)] += y[r][i] * x[i][c]  # remember that mat4 mults are flipped to support right side vec4 mults
        
        for r in range(0,4):
            for c in range(0,4):
                self.assertEqual(xy[r][c],data[idx(r,c)])        
            


def main():
    unittest.main()





if __name__=='__main__':
    main()