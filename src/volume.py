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
from log import log



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
		self.determineNeighbors()


	def determineNeighbors(self):
		def findNeighbor(v0, v1):
			ret = None
			for i in range(len(self.triangles)):
				tri = self.triangles[i]
				isNeighbor = \
					(tri[0] == v1 and tri[1] == v0) or \
					(tri[1] == v1 and tri[2] == v0) or \
					(tri[2] == v1 and tri[0] == v0)
				if isNeighbor:
					if not(ret is None):
						raise Exception(
							'Mesh is not a proper volume description: '
							'there is a triangle with multiple neighbors on one side')
					ret = i

			if ret is None:
				raise Exception(
					'Mesh is not a proper volume description: '
					'there is a triangle without a neighbor on one side')
			return ret

		self.neighbors = \
		[
			[
			findNeighbor(tri[0], tri[1]),
			findNeighbor(tri[1], tri[2]),
			findNeighbor(tri[2], tri[0])
			]
		for tri in self.triangles
		]


	def splitInsideOutside(self, otherMesh):
		planes = getTrianglesByPlane(otherMesh)
		for plane, triangles in planes:
			#sys.stderr.write('%s\n' % str(plane))
			intersections = self.getPlaneIntersections(plane)
		return otherMesh, otherMesh #TODO


	def getPlaneIntersections(self, plane):
		planeNormal = plane.normal()
		planePos    = plane.length()

		ret = []

		for tri in self.triangles:
			tri = [self.vertices[k] for k in tri]
			relPos = [v.dotProduct(planeNormal) - planePos for v in tri]

			#If the triangle is entirely on one side of the plane,
			#it does not intersect -> ignore this triangle
			side = [p > 0.0 for p in relPos]
			if False not in side or True not in side:
				continue

			#Keep permutating vertices until 0->1 is a neg->pos transition
			while relPos[0] > 0.0 or relPos[1] < 0.0:
				relPos = [relPos[1], relPos[2], relPos[0]]
				tri    = [   tri[1],    tri[2],    tri[0]]

			#The neg->pos transition point
			f = relPos[1] / (relPos[1] - relPos[0])
			p0 = f * tri[0] + (1-f) * tri[1]

			#Now, the pos->neg transition is in either 1->2 or 2->0
			if relPos[2] > 0.0: #2->0
				f = relPos[2] / (relPos[2] - relPos[0])
				p1 = f * tri[0] + (1-f) * tri[2]
			else:               #1->2
				f = relPos[1] / (relPos[1] - relPos[2])
				p1 = f * tri[2] + (1-f) * tri[1]

			ret.append((p0, p1))

		#TODO: detect loops?
		return ret

