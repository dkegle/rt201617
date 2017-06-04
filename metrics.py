from math import sqrt

def get_distance_matrix(texts, metric):
	""" Compute the distance matrix for a given metric.
	"""
	n = len(texts)
	mat = [[0 for _ in range(n)] for _ in range(n)]
	for i in range(n):
		for j in range(i, n):
			d = metric(texts[i], texts[j])
			mat[i][j] = d
			mat[j][i] = d
	return mat

def hellinger_dist(text1, text2):
	h1 = text1.histogram
	h2 = text1.histogram
	n1 = max(h1.keys())
	n2 = max(h2.keys())

	return sqrt(1/2 * sum((sqrt(h1[i])-sqrt(h2[i]))**2 for i in range(min(n1, n2))))

def chisq_dist(text1, text2):
	h1 = text1.histogram
	h2 = text1.histogram
	n1 = max(h1.keys())
	n2 = max(h2.keys())

	return 1/2 * sum(([h1[i] - h2[i]])^2 / (h1[i] + h2[i] + 1e-10))

def euclidean_dist(text_1, text_2):
	return sqrt(sum([(x1-x2)**2 for x1,x2 in zip(text_1.asVector(), text_2.asVector())]))
