#!/usr/bin/env python3
#    stlcat.py
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

import mesh
import stl

totalMesh = mesh.Mesh()

for filename in sys.argv:
	with open(filename, 'rb') as f:
		subMesh = stl.load(f)
		#TODO: add to totalMesh

stl.save(sys.stdout, totalMesh)

