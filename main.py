from text_parser import TextParser
import metrics as m
from processing import TextComplex, AbstractTextComplex
from os import listdir, path, devnull
import numpy as np
import time
import sys
from matplotlib import pyplot as plt

plt.rcParams["figure.figsize"] = (6,6)
plt.rcParams["savefig.directory"] = "plots"

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
		#plt.savefig("plots/barcodes/" + cx.name.split("/")[1] + ".pdf", dpi=100)
		cx.plot_persistence_diagram(dim)

def get_barcode_plot(cx, name=None):
	colors = {0: "red",
		  1: "green",
		  2: "blue",
		  3: "teal",
		  4: "magenta",
		  5: "yellow"}

	# Spli the diagram into dims.
	dims = sorted(list(set([d[0] for d in cx.diag])))
	dimdiag = {}
	for dim in dims:
		dimdiag[dim] = ([d[1] for d in cx.diag if d[0] == dim])

	# Create plot.
	fig, ax = plt.subplots()

	y = 1
	maxx = -1
	for dim in dims:
		ys = []
		xmins = []
		xmaxs = []
		for diag in dimdiag[dim]:
			if diag[1] == float("inf"):
				diag = (diag[0], 1e10)
			elif diag[1] > maxx:
				maxx = diag[1]
			xmins.append(diag[0])
			xmaxs.append(diag[1])
			ys.append(y)
			y += 1

		ax.hlines(y=ys, xmin=xmins, xmax=xmaxs,
			  linewidth=200 // len(cx.diag),
                          color = colors[dim],
			  label="dim = " + str(dim))
	ax.set_ylim([0.5, y+0.5])
	ax.set_xlim([-maxx*0.1, maxx*1.1])
	ax.legend()
	ax.get_yaxis().set_visible(False)
	if name == None:
		fig.suptitle(cx.name.split("/")[-1])
	else:
		fig.suptitle(name)
	return fig, ax


if __name__ == "__main__":

	f = open(devnull, "w")
	sys.stdout = f
	cxs_alpha = read_cxs("data", None)
	mat_alpha, names = bottleneck_distance_matrix(cxs_alpha)
	cxs_rips = read_cxs("data", m.euclidean)
	mat_rips, _ = bottleneck_distance_matrix(cxs_rips)
	sys.stdout = sys.__stdout__;
	f.close()

	print("=======================================================================")
	print("Alpha complex:")
	print(names)
	print(mat_alpha)
	print()
	print("=======================================================================")
	print("Rips complex:")
	print(names)
	print(mat_rips)

	for dist_word, dist_sent in zip([m.hellinger_word, m.chisq_word, m.euclidean_hist_word],
					[m.hellinger_sent, m.chisq_sent, m.euclidean_hist_sent]):
		# Suppress printing
		f = open(devnull, "w")
		sys.stdout = f
		cxs_word = read_cxs("data", dist_word)
		cxs_sent = read_cxs("data", dist_sent)
		mat_word, names = bottleneck_distance_matrix(cxs_word)
		mat_sent, _ = bottleneck_distance_matrix(cxs_sent)
		sys.stdout = sys.__stdout__;
		f.close()
		print()
		print("=======================================================================")
		print("Rips complex with " + str(dist_word) + ":")
		print("word:")
		print(names)
		print(mat_word)
		print("sentence:")
		print(names)
		print(mat_sent)

	fig,ax = get_barcode_plot(cxs_alpha[0], "Old Testament")
	fig.savefig("plots/barcodes/bible-old.pdf")
	fig,ax = get_barcode_plot(cxs_alpha[2], "phys.org")
	fig.savefig("plots/barcodes/phys.pdf")
	fig,ax = get_barcode_plot(cxs_alpha[3], "Recipes")
	fig.savefig("plots/barcodes/recipes.pdf")
	fig,ax = get_barcode_plot(cxs_alpha[4], "New Testament")
	fig.savefig("plots/barcodes/bible-new.pdf")
