from text_parser import TextParser
from os import listdir
from os import path
import time

line_stop = ".!?"
word_split = " ,"

def read_data(dirpath, line_stop=".!?", word_split=" ,",
	      stop_words = False, stop_word_file = "data/stop-words.txt"):

	""" Parse all *.txt files in subdirectories of dirpath and return a list
	of features.
	"""
	res = []
	subdirs = [path.join(dirpath, d) for d in listdir(dirpath)
		   if path.isdir(path.join(dirpath, d))]
	for d in subdirs:
		print("reading %s..." % d)
		txt_files = [path.join(d, p) for p in listdir(d) if p.endswith(".txt")]
		tp = TextParser(txt_files, line_stop, word_split, stop_words, stop_word_file)
		tp.run()
		res.append([txt.asVector() for txt in tp.getResults()])

	return res


if __name__ == "__main__":
	texts = read_data("data")
	print(texts)
