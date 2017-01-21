#!/usr/bin/env python3
#    stltranslate.py
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

from mesh import Vector
import stl

t = Vector(float(sys.argv[-4]), float(sys.argv[-3]), float(sys.argv[-2]))

with open(sys.argv[-1], 'rb') as f:
	mesh = stl.load(f)

mesh.vertices = \
[
	v + t
	for v in mesh.vertices
]

stl.save(sys.stdout.buffer, mesh)

