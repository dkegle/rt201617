from text_parser import TextParser
import metrics as m
from processing import TextComplex, AbstractTextComplex
from os import listdir, path, devnull
import numpy as np
import time
import sys
from matplotlib import pyplot as plt

# Better formatting
np.set_printoptions(formatter={'float': '{: 0.3f}'.format})

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
			res.append(m.distance_matrix(text_set, metric))
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

def bottleneck_distance_matrix(cxs):
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
	cxs_alpha = read_cxs("data", None)
	mat_alpha = bottleneck_distance_matrix(cxs_alpha)

	for dist in [m.hellinger_word, m.chisq_word, m.euclidean_hist_word,
		     m.hellinger_sent, m.chisq_sent, m.euclidean_hist_sent,
		     m.euclidean]:
		# Suppress printing
		f = open(devnull, "w")
		sys.stdout = f
		cxs = read_cxs("data", dist)
		mat = bottleneck_distance_matrix(cxs)
		sys.stdout = sys.__stdout__;
		f.close()
		print("Distance: " + str(dist))
		print(mat)
