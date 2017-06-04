from text_parser import TextParser
from metrics import get_distance_matrix, hellinger_dist, chisq_dist, euclidean_dist
from processing import TextComplex, AbstractTextComplex
from os import listdir
from os import path
import numpy as np
import time
from matplotlib import pyplot as plt

line_stop = ".!?"
word_split = " ,"

def read_data(dirpath, metric = None, line_stop=".!?", word_split=" ,",
	      stop_words = False, stop_word_file = "data/stop-words.txt"):

	""" Parse all *.txt files in subdirectories of dirpath and return a list
	of features.
	"""
	text_sets, names = [], []

	subdirs = [path.join(dirpath, d) for d in listdir(dirpath)
		   if path.isdir(path.join(dirpath, d))]

	for d in subdirs:
		print("reading %s..." % d)
		txt_files = [path.join(d, p) for p in listdir(d) if p.endswith(".txt")]
		tp = TextParser(txt_files, line_stop, word_split, stop_words, stop_word_file)
		tp.run()
		text_sets.append(tp.getResults())
		names.append(d)

	res = []
	if metric:
		# distance matrices (for each complex)
		res = []
		for text_set in text_sets:
			global ts
			ts = text_set
			res.append(get_distance_matrix(text_set, metric))
	else:
		res = [[txt.asVector() for txt in text_set] for text_set in text_sets]

	return res, names

def read_cxs(dirpath, metric = None, *args):
	""" Read a list of TextComplex from directory.
	"""
	if metric:
		texts, names = read_data(dirpath, metric, *args)
		return [AbstractTextComplex(m, n) for m,n in zip(texts, names)]
	else:
		texts, names = read_data(dirpath, None, *args)
		return [TextComplex(t, n) for t,n in zip(texts, names)]

def distance_matrix(cxs):
	""" for bottleneck distance between diagrams """
	mat = np.zeros((len(cxs), len(cxs)))

	for i, ci in enumerate(cxs):
		for j, cj in enumerate(cxs):
			dist = ci.bottleneck_distance_to(cj)
			print("d(%s, %s) = %f" % (ci.name, cj.name, dist))

			mat[i,j] = dist

	return mat, [c.name for c in cxs]

def plot_diagrams(cxs, dim=0):
	for cx in cxs:
		print(cx.name)
		cx.plot_persistence_barcode(dim)
		cx.plot_persistence_diagram(dim)



if __name__ == "__main__":
	cxs = read_cxs("data", None)
	cxs_hell = read_cxs("data", hellinger_dist)
	mat = distance_matrix(cxs)
	print(mat)
