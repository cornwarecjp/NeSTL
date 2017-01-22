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

import math

from log import log



class Vector(list):
	def __init__(self, x=0.0, y=0.0, z=0.0):
		list.__init__(self, (x,y,z))


	def __add__(self, v):
		return Vector(self[0]+v[0], self[1]+v[1], self[2]+v[2])


	def __sub__(self, v):
		return Vector(self[0]-v[0], self[1]-v[1], self[2]-v[2])


	def __rmul__(self, s):
		return Vector(s*self[0], s*self[1], s*self[2])


	def scale(self, v):
		return Vector(self[0]*v[0], self[1]*v[1], self[2]*v[2])


	def dotProduct(self, v):
		return self[0]*v[0] + self[1]*v[1] + self[2]*v[2]


	def crossProduct(self, v):
		return Vector(
			self[1]*v[2] - self[2]*v[1],
			self[2]*v[0] - self[0]*v[2],
			self[0]*v[1] - self[1]*v[0]
			)


	def length(self):
		return math.sqrt(self[0]**2 + self[1]**2 + self[2]**2)


	def normal(self):
		return (1.0/self.length()) * self
		

	def equals(self, other, maxError=1e-6):
		err = [abs(other[k] - self[k]) for k in range(3)]
		return max(err) <= maxError



class Plane:
	def __init__(self, normal, distance):
		self.normal = normal
		self.distance = distance

	def equals(self, other, maxError=1e-6):
		return self.normal.equals(other.normal, maxError) and \
			abs(self.distance - other.distance) <= maxError



class Mesh:
	def __init__(self):
		self.vertices = []
		self.triangles = []


	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return '\n'.join([str(x) for x in self.vertices + self.triangles])


	def removeDoubleVertices(self):
		maxError=1e-6

		#As an optimization, before checking vertices, make a list of
		#vertex indices that is sorted on coordinate bins.
		#Then, only compare vertex pairs that are close on this list.
		#Bin size is 1 * maxError. The trade-off is:
		# - larger bin size: increases the likelihood that non-matching vertices
		#                    end up in the same bin; this could prevent matching
		#                    vertices in that bin from being matched.
		# - smaller bin size: increases the likelihood that matching vertices
		#                     end up in different bins; this would prevent those
		#                     vertices from being matched.
		sortedVertexList = list(range(len(self.vertices)))
		sortedVertexList.sort(key=lambda i: math.floor(self.vertices[i][0]/maxError))
		sortedVertexList.sort(key=lambda i: math.floor(self.vertices[i][1]/maxError))
		sortedVertexList.sort(key=lambda i: math.floor(self.vertices[i][2]/maxError))
		self.removeDoubleVertices_sortList(sortedVertexList, maxError)

		# do it again, with shifted bins:
		sortedVertexList = list(range(len(self.vertices)))
		sortedVertexList.sort(key=lambda i: math.floor(0.5+self.vertices[i][0]/maxError))
		sortedVertexList.sort(key=lambda i: math.floor(0.5+self.vertices[i][1]/maxError))
		sortedVertexList.sort(key=lambda i: math.floor(0.5+self.vertices[i][2]/maxError))
		self.removeDoubleVertices_sortList(sortedVertexList, maxError)


	def removeDoubleVertices_sortList(self, sortedVertexList, maxError):
		log('Before: %dv, %dt' % (len(self.vertices), len(self.triangles)))
		if len(self.vertices) < 2:
			return

		for i_sorted in range(len(self.vertices)-1):
			if i_sorted >= len(self.vertices)-1:
				break
			i = sortedVertexList[i_sorted]
			v_i = self.vertices[i]
			#log('i: ' + str(v_i))
			for j_sorted in range(i_sorted+1, len(self.vertices)):
				if j_sorted >= len(self.vertices):
					break
				j = sortedVertexList[j_sorted]
				v_j = self.vertices[j]
				#log('    j: ' + str(v_j))

				if not v_j.equals(v_i, maxError):
					break

				#It's a double
				#log('    double')

				#Assign average to first vertex
				avg = [0.5*(v_j[k] + v_i[k]) for k in range(3)]
				v_i[0] = avg[0]
				v_i[1] = avg[1]
				v_i[2] = avg[2]

				#Remove second vertex
				del self.vertices[j]
				del sortedVertexList[j_sorted]

				#Replace references to second vertex, and rewrite higher indices
				for tri in self.triangles:
					for k in range(3):
						if tri[k] > j:
							tri[k] -= 1
						elif tri[k] == j:
							tri[k] = i
				for k in range(len(sortedVertexList)):
					if sortedVertexList[k] > j:
						sortedVertexList[k] -= 1

		#Remove triangles that have become lines or points
		self.triangles = list(filter(
			lambda tri: tri[0] != tri[1] and tri[1] != tri[2] and tri[2] != tri[0],
			self.triangles))

		log('After: %dv, %dt' % (len(self.vertices), len(self.triangles)))

