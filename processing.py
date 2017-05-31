import gudhi as gd

class TextComplex:

	def __init__(self, pts, name="", max_alpha_square=0.5):
		""" Build Processor from list of points (list of lists of numbers)
		"""
		self.pts = pts
		self.name = name
		self.alpha = gd.AlphaComplex(points = pts)
		self.max_alpha_square = max_alpha_square

		print("Building %s..." % name)
		self.sxtree = self.alpha.create_simplex_tree(max_alpha_square = self.max_alpha_square)
		print("Number of sx's: %d" % self.sxtree.num_simplices())

		self.diag = self.sxtree.persistence()

	def __repr__(self):
		return "TextComplex(" + self.name + ")"

	def plot_persistence_diagram(self, dim=0):
		""" Plot persistence diagram.
		"""
		selfdiag = [x for x in self.diag if x[0] == dim]
		gd.plot_persistence_diagram(selfdiag)

	def plot_persistence_barcode(self, dim=0):
		""" Plot barcode diagram.
		"""
		selfdiag = [x for x in self.diag if x[0] == dim]
		gd.plot_persistence_barcode(selfdiag)

	def bottleneck_distance_to(self, other, dim=0, e=0):
		""" Compute the bottleneck distance to antoher TextComplex.
		"""
		if not isinstance(other, TextComplex):
			raise "Invalid paramter!"

		selfdiag = [x[1] for x in self.diag if x[0] == dim]
		otherdiag = [x[1] for x in other.diag if x[0] == dim]

		return gd.bottleneck_distance(selfdiag, otherdiag, e)

	def betti_numbers(self):
		""" Return the betti numbers of TextComplex.
		"""
		return self.sxtree.betti_numbers()
