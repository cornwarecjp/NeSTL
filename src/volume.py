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

#import sys

from mesh import Mesh



def getTrianglePlane(tri):
	v1 = tri[1] - tri[0]
	v2 = tri[2] - tri[1]
	normal = v1.crossProduct(v2).normal()
	distance = tri[0].dotProduct(normal)
	return distance * normal


def getTrianglesByPlane(sourceMesh):
	ret = []
	for tri in sourceMesh.triangles:
		tri = [sourceMesh.vertices[k] for k in tri]
		triPlane = getTrianglePlane(tri)
		found = False
		for plane, planeTriangles in ret:
			if plane.equals(triPlane):
				planeTriangles.append(tri)
				found = True
				break
		if not found:
			ret.append((triPlane, [tri]))
	return ret



class Volume(Mesh):
	def __init__(self, sourceMesh):
		Mesh.__init__(self)
		self.vertices  = sourceMesh.vertices[:]
		self.triangles = sourceMesh.triangles[:]


	def getOutsidePart(self, otherMesh):
		planes = getTrianglesByPlane(otherMesh)
		#for pl,tr in planes:
		#	sys.stderr.write('%s\n' % str(pl))
		return otherMesh #TODO


	def getInsidePart(self, otherMesh):
		planes = getTrianglesByPlane(otherMesh)
		return otherMesh #TODO

