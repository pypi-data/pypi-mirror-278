# VectorAnalysis
This is a tutorial on how to use a PyPI application.
You can culculate gradient, divergence and curl by using this application.

# How to install VectorAnalysis
$ pip install VectorAnalysis

# How to run VectorAnalysis
You need also "sympy" to run this application.
$ pip install sympy

example:
In [1]: from sympy.vector import CoordSys3D
In [2]: C = CoordSys3D('C')
In [3]: g = C.x * C.y * C.z
In [4]: gradient(g)
Out[4]: C.y*C.z*C.i + C.x*C.z*C.j + C.x*C.y*C.k