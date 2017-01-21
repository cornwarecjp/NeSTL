#    volume.py
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

from mesh import Mesh



class Volume(Mesh):
	def __init__(self, sourceMesh):
		Mesh.__init__(self)
		self.vertices  = sourceMesh.vertices[:]
		self.triangles = sourceMesh.triangles[:]


	def getOutsidePart(self, otherMesh):
		return otherMesh #TODO


	def getInsidePart(self, otherMesh):
		return otherMesh #TODO

