import numpy as np
from math import sqrt

def distance_matrix(texts, metric):
	""" Compute the distance matrix for a given metric.
	"""
	n = len(texts)
	mat = np.zeros((n,n))
	for i in range(n):
		for j in range(i, n):
			d = metric(texts[i], texts[j])
			mat[i,j] = d
			mat[j,i] = d
	return mat

def gethists(text1, text2, word):
	if word:
		h1 = text1.word_histogram
		h2 = text2.word_histogram
	else:
		h1 = text1.sent_histogram
		h2 = text2.sent_histogram
	n1 = max(h1.keys())
	n2 = max(h2.keys())

	return h1, h2, max(n1, n2)

def hellinger_aux(text1, text2, word):
	h1, h2, n = gethists(text1, text2, word)
	return sqrt(1/2 * sum((sqrt(h1[i])-sqrt(h2[i]))**2 for i in range(n)))

def hellinger_word(text1, text2):
	return hellinger_aux(text1, text2, True)

def hellinger_sent(text1, text2):
	return hellinger_aux(text1, text2, False)

def chisq_aux(text1, text2, word):
	h1, h2, n = gethists(text1, text2, word)
	return 1/2 * sum((h1[i] - h2[i])**2 / (h1[i] + h2[i] + 1e-10) for i in range(n))

def chisq_word(text1, text2):
	return chisq_aux(text1, text2, True)

def chisq_sent(text1, text2):
	return chisq_aux(text1, text2, False)

def euclidean_hist_aux(text1, text2, word):
	"""
	Euclidean distance between histograms.
	"""
	h1, h2, n = gethists(text1, text2, word)
	return sqrt(sum((h1[i] - h2[i])**2 for i in range(n)))

def euclidean_hist_word(text1, text2):
	return euclidean_hist_aux(text1, text2, True)

def euclidean_hist_sent(text1, text2):
	return euclidean_hist_aux(text1, text2, False)

def euclidean(text1, text2):
	return sqrt(sum([(x1-x2)**2 for x1,x2 in zip(text1.asVector(), text2.asVector())]))
