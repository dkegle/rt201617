from math import log, sqrt
from collections import Counter
import re

class Text:
	text_file = ""
	avgWordRatio = 0.0 # average word length / longest word length
	avgSentenceRatio = 0.0 # average sentence length / longest sentence length
	tfidfRatio = 0.0 # num of three top idf words / num of all words
	atMostEightRatio = 0.0 # num of words with at most eight chars / num of all words
	atLeastNineRatio = 0.0 # num of words with at least nine chars / num of all words
	diversityRatio = 0.0 # num of different words / num of all words

	def asVector(self):
		return (self.avgWordRatio,
				self.avgSentenceRatio,
				self.tfidfRatio,
				self.atMostEightRatio,
				self.atLeastNineRatio,
				self.diversityRatio)

	def __repr__(self):
		return "Text(" + self.text_file + ")"

class TextParser:
	texts = []
	text_paths = []
	line_stop = ""
	word_split = ""
	stop_words = []

	def __init__(self, text_paths, line_stop=".!?", word_split=" ,",
		     stop_words = False, stop_word_file = "data/stop-words.txt"):
		""" text_paths is a list of strings, which stores paths to files
		that will be parsed.
		line_stop and word_split are delimiters for sentences and words.

		examples:
			tp = TextParser(["data/text1.txt", "data/text2.txt"])
			tp2 = TextParser(["data/text1.txt", "data/text2.txt"], ".!?", " ,")
		"""
		if not (isinstance(text_paths, list) and isinstance(line_stop, str) and isinstance(word_split, str)):
			raise "Invalid init parameters"
		for text in text_paths:
			if not isinstance(text, str):
				raise "Invalid init parameters"

		self.text_paths = text_paths
		self.line_stop = line_stop
		self.word_split = word_split

		if stop_words:
			f = open(stop_word_file)
			self.stop_words = f.read().split("\n")
			f.close()
		else:
			self.stop_words = []


	def run(self):
		word_frequencies = {} # needed for tf-idf
		for text in self.text_paths:
			try:
				# parse whole text into single string
				f = open(text, "r")
				big_string = " ".join([line for line in f])
				f.close()

				# split it into sentences
				sentences = re.split("[" + self.line_stop + "]", big_string)
				num_of_sentences = len([s for s in sentences if len(s) > 0])

				# loop through sentences
				total_sentence_length = 0.0
				longest_sentence_length = 0.0
				total_word_length = 0.0
				longest_word_length = 0.0
				at_most_eight = 0.0
				at_least_nine = 0.0
				words_in_text = []
				for sentence in sentences:
					# split sentence into words
					sentence_words = re.split("[" + self.word_split + "]", sentence)
					sentence_words = [w for w in sentence_words if len(w) > 0 and not w in self.stop_words]

					# update parameters
					words_in_text += sentence_words
					total_sentence_length += len(sentence_words)
					if len(sentence_words) > longest_sentence_length:
						longest_sentence_length = len(sentence_words)

					for w in sentence_words:
						total_word_length += len(w)
						if len(w) > longest_word_length:
							longest_word_length = len(w)

					at_most_eight += len([w for w in sentence_words if 0 < len(w) <= 8])
					at_least_nine += len([w for w in sentence_words if len(w) >= 9])

				# save information about new text
				new_text = Text()
				avg_sentence_length = total_sentence_length / num_of_sentences
				new_text.avgSentenceRatio = avg_sentence_length / longest_sentence_length

				num_of_words = float(len(words_in_text))

				avg_word_length = total_word_length / num_of_words
				new_text.avgWordRatio = avg_word_length / num_of_words

				new_text.atMostEightRatio = at_most_eight / num_of_words
				new_text.atLeastNineRatio = at_least_nine / num_of_words

				new_text.diversityRatio = len(set(words_in_text)) / num_of_words

				new_text.text_file = text

				c = dict(Counter(words_in_text))
				word_frequencies[new_text] = {word: c[word]/num_of_words \
					for word in words_in_text}

				self.texts.append(new_text)
			except Exception as e:
				print("Failed to load " + text)
				print(str(e))
				print("Skipping to next file")

		# calculate tf-idf
		word_idf = {}
		for text in self.texts:
			tfidf = {}
			for word in word_frequencies[text]:
				if word not in word_idf:
					num_appearances = 0
					for s in self.texts:
						if word in word_frequencies[s]:
							num_appearances += 1
					word_idf[word] = log(len(self.texts) / float(num_appearances))
				tfidf[word] = word_frequencies[text][word] * word_idf[word]

			highest_tfidf = sorted(tfidf, key=tfidf.get(1))[-3:]
			text.tfidfRatio = sum([word_frequencies[text][w] for w in highest_tfidf])


	def getResults(self):
		return self.texts
