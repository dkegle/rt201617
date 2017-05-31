from text_parser import TextParser
from processing import TextComplex
from os import listdir
from os import path
import numpy as np
import time

line_stop = ".!?"
word_split = " ,"

def read_data(dirpath, line_stop=".!?", word_split=" ,",
	      stop_words = False, stop_word_file = "data/stop-words.txt"):

	""" Parse all *.txt files in subdirectories of dirpath and return a list
	of features.
	"""
	res = []
	names = []
	subdirs = [path.join(dirpath, d) for d in listdir(dirpath)
		   if path.isdir(path.join(dirpath, d))]
	for d in subdirs:
		print("reading %s..." % d)
		txt_files = [path.join(d, p) for p in listdir(d) if p.endswith(".txt")]
		tp = TextParser(txt_files, line_stop, word_split, stop_words, stop_word_file)
		tp.run()
		res.append([txt.asVector() for txt in tp.getResults()])
		names.append(d)

	return res, names

def distance_matrix(dirpath, *args):
	texts, names = read_data(dirpath, *args)
	cxs = []
	mat = np.zeros((len(texts), len(texts)))

	for i in range(len(texts)):
		cxs.append(TextComplex(texts[i], names[i]))

	for i in range(len(texts)):
		for j in range(len(texts)):
			dist = cxs[i].bottleneck_distance_to(cxs[j])
			print("d(%s, %s) = %f" % (names[i], names[j], dist))

			mat[i,j] = dist

	return mat, names


if __name__ == "__main__":
	texts = read_data("data")
	print(texts)
