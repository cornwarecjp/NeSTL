#    mesh.py
#    Copyright (C) 2017 by CJP
#
#    This file is part of NeSTL.
#
#    NeSTL is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    NeSTL is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with NeSTL. If not, see <http://www.gnu.org/licenses/>.


class Vector(list):
	def __init__(self, x=0.0, y=0.0, z=0.0):
		list.__init__(self, (x,y,z))

	def scale(self, v):
		return Vector(self[0]*v[0], self[1]*v[1], self[2]*v[2])


	def __add__(self, v):
		return Vector(self[0]+v[0], self[1]+v[1], self[2]+v[2])



class Mesh:
	def __init__(self):
		self.vertices = []
		self.triangles = []


	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return '\n'.join([str(x) for x in self.vertices + self.triangles])

