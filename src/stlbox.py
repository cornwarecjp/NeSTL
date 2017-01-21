#!/usr/bin/env python3
#    stlbox.py
#    Copyright (C) 2017 by CJP
#
#    This file is part of NeSTL.
#
#    NeSTL is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License.
#    (at your option) any later version.
#
#    NeSTL is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with NeSTL. If not, see <http://www.gnu.org/licenses/>.

import sys

from mesh import Mesh, Vector
import stl

size = Vector(float(sys.argv[-3]), float(sys.argv[-2]), float(sys.argv[-1]))

box = Mesh()

#Vertices
box.vertices = \
[
	Vector(-0.5, -0.5, -0.5),
	Vector(-0.5, -0.5,  0.5),
	Vector(-0.5,  0.5, -0.5),
	Vector(-0.5,  0.5,  0.5),
	Vector( 0.5, -0.5, -0.5),
	Vector( 0.5, -0.5,  0.5),
	Vector( 0.5,  0.5, -0.5),
	Vector( 0.5,  0.5,  0.5)
]
box.vertices = [v.scale(size) for v in box.vertices]

#Triangles
box.triangles = \
[
	[0,2,6], [0,6,4],
	[0,4,5], [0,5,1],
	[4,6,7], [4,7,5],
	[6,2,3], [6,3,7],
	[2,0,1], [2,1,3],
	[1,5,7], [1,7,3]
]

stl.save(sys.stdout.buffer, box)

