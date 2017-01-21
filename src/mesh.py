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

#import sys
import math



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


	def normal(self):
		size = math.sqrt(self[0]**2 + self[1]**2 + self[2]**2)
		return (1.0/size) * self
		

	def equals(self, other, maxError=1e-6):
		avg = [0.5*(other[k] + self[k]) for k in range(3)]
		err = \
		[
			abs(other[k] - self[k]) /
			(abs(avg[k]) + 1e-38) #prevent division by zero
		for k in range(3)
		]

		return max(err) <= maxError



class Mesh:
	def __init__(self):
		self.vertices = []
		self.triangles = []


	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return '\n'.join([str(x) for x in self.vertices + self.triangles])


	def removeDoubleVertices(self):
		#sys.stderr.write('Before: %d\n' % len(self.vertices))
		if len(self.vertices) < 2:
			return

		for i in range(len(self.vertices)-1):
			if i >= len(self.vertices)-1:
				break
			v_i = self.vertices[i]
			#sys.stderr.write('i=%d: %s\n' % (i, str(v_i)))
			for j in range(i+1, len(self.vertices)):
				while j < len(self.vertices):
					v_j = self.vertices[j]
					#sys.stderr.write('j=%d: %s\n' % (j, str(v_j)))

					if not v_j.equals(v_i):
						break #break from while -> continue with next j
					#It's a double
					#sys.stderr.write('double\n')

					#Assign average to first vertex
					avg = [0.5*(v_j[k] + v_i[k]) for k in range(3)]
					v_i[0] = avg[0]
					v_i[1] = avg[1]
					v_i[2] = avg[2]

					#Remove second vertex
					del self.vertices[j]

					#Replace references to second vertex
					for tri in self.triangles:
						for k in range(3):
							if tri[k] > j:
								tri[k] -= 1
							elif tri[k] == j:
								tri[k] = i
		#sys.stderr.write('After: %d\n' % len(self.vertices))

