from text_parser import TextParser

text_paths = [
#	"data/phys.org/1.txt",
	"data/phys.org/2.txt",
#	"data/phys.org/3.txt",
#	"data/phys.org/4.txt",
#	"data/phys.org/5.txt",
#	"data/phys.org/6.txt",
#	"data/phys.org/7.txt",
#	"data/phys.org/8.txt",
#	"data/phys.org/9.txt",
#	"data/phys.org/10.txt",
#	"data/bible-newtest.txt",
#	"data/bible-oldtest.txt"
]

line_stop = ".!?"
word_split = " ,"

if __name__ == "__main__":

	texts = []
	tp = TextParser(text_paths, line_stop, word_split)
	tp.run()
	texts = tp.getResults()
	for text in texts:
		print("Text: " + text.text_file)
		print("Value: " + str(text.asVector()) + "\n")