import numpy
from math import *
import math
# w tym dziale miałem największy fun
def pi():
    numpy.pi()
def square_circuit(x,y):
    xc = int(x)
    yc = int(y)
    return xc+yc * 2
def triangle_circuit(x,y,z):
    xc = int(x)
    yc = int(y)
    zc = int(z)
    return xc+yc+zc
def pitagoras_math(a,b):
    a = float(a)
    b = float(b)
    o = sqrt(a**2 + b**2)
    return o 