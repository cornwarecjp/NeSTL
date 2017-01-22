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

import math

from mesh import Mesh, Plane
from log import log



def getTrianglePlane(tri):
	v1 = tri[1] - tri[0]
	v2 = tri[2] - tri[1]
	normal = v1.crossProduct(v2).normal()
	distance = tri[0].dotProduct(normal)
	return Plane(normal, distance)


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


def getNumLoops(vtx, normal, loop):
	loop = loop[:] + [loop[0]]
	totalAngle = 0
	for i in range(len(loop)-1):
		p0 = loop[i]   - vtx
		p1 = loop[i+1] - vtx
		crossProd = p1.crossProduct(p0).dotProduct(normal) #|p0||p1|sin(a)
		totalAngle += math.asin(crossProd / (p0.length()*p1.length()))

	numLoops = totalAngle / (2*math.pi)
	#log(numLoops)
	return math.floor(numLoops + 0.5) #round to nearest



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
		insideMesh = Mesh()
		outsideMesh = Mesh()

		planes = getTrianglesByPlane(otherMesh)
		for plane, triangles in planes:
			intersections = self.getPlaneIntersections(plane)

			insideTriangles = []
			outsideTriangles = []
			for tri in triangles:
				#Check for one vertex whether it's inside or outside
				totalNumLoops = sum(
				[
				getNumLoops(tri[0], plane.normal, loop)
				for loop in intersections
				])
				if totalNumLoops > 0:
					insideTriangles.append(tri)
				elif totalNumLoops == 0:
					outsideTriangles.append(tri)
				else: # totalNumLoops < 0:
					raise Exception(
						'Unexpected negative number of loops. '
						'Maybe the volume is inside-out?'
						)
			
		return otherMesh, otherMesh #TODO


	def getPlaneIntersections(self, plane):
		ret = []

		notYetProcessed = list(range(len(self.triangles)))
		while len(notYetProcessed) > 0:
			startIndex = notYetProcessed.pop(0)

			vtx = [self.vertices[k] for k in self.triangles[startIndex]]
			relPos = [v.dotProduct(plane.normal) - plane.distance for v in vtx]
			nb = self.neighbors[startIndex][:] #load copy of neighbors

			#If the triangle is entirely on one side of the plane,
			#it does not intersect -> ignore this triangle
			side = [p > 0.0 for p in relPos]
			if False not in side or True not in side:
				continue

			loop = []

			triIndex = startIndex
			while True:
				#Keep permutating vertices until 0->1 is a neg->pos transition
				while relPos[0] > 0.0 or relPos[1] < 0.0:
					relPos = [relPos[1], relPos[2], relPos[0]]
					vtx    = [   vtx[1],    vtx[2],    vtx[0]]
					nb     = [    nb[1],     nb[2],     nb[0]]

				#The neg->pos transition point (add to the loop)
				f = relPos[1] / (relPos[1] - relPos[0])
				loop.append(f * vtx[0] + (1-f) * vtx[1])

				#Now, the pos->neg transition is in either 1->2 or 2->0
				if relPos[2] > 0.0: #2->0
					triIndex = nb[2]
				else:               #1->2
					triIndex = nb[1]

				#Stop if start index is reached (end of loop):
				if triIndex == startIndex:
					break

				#We'll be processing it now, so don't do it later again:
				notYetProcessed.remove(triIndex)

				#Load new triangle (for next iteration)
				vtx = [self.vertices[k] for k in self.triangles[triIndex]]
				relPos = [v.dotProduct(plane.normal) - plane.distance for v in vtx]
				nb = self.neighbors[triIndex][:] #load copy of neighbors

			ret.append(loop)

		return ret

