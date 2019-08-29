import re

"""

Document object

Keeps 

"""
class Document:

	# TODO: give documents names?
	def __init__(self, text):
		self.text = text
		# keep only characters and whitespace
		# TODO: currently ignores special characters
		# TODO: should the letters be lowercased?
		self.clean_text = re.sub('[^a-zA-Z\s]+', '', text)
		self.all_words = self.clean_text.split() # split by whitespace
		self.unique_words = set(self.all_words)
		self.counts = { word : 0 for word in self.unique_words }
		for word in self.all_words:
			self.counts[word] = self.counts[word] + 1

# module method
def read_from_txt(file):
	# TODO: currently assumes file is a text file
	with open(file, 'r') as f:
		text = f.read()
		return Document(text)


# test
if __name__ == '__main__':
	
	# simple example
	doc = Document('Hello World')
	assert(doc.clean_text == 'Hello World')
	assert(doc.unique_words == set(['Hello', 'World']))
	assert(doc.counts == { 'Hello': 1, 'World': 1 })

	# with punction
	doc = Document('Hello. World!')
	assert(doc.clean_text == 'Hello World')
	assert(doc.unique_words == set(['Hello', 'World']))
	assert(doc.counts == { 'Hello': 1, 'World': 1 })

	# from file
	doc = read_from_txt('./test_docs/doc1.txt')
	assert(doc.clean_text == 'Hello World')
	assert(doc.unique_words == set(['Hello', 'World']))
	assert(doc.counts == { 'Hello': 1, 'World': 1 })

	# with duplicate words
	doc = Document('I like words, and more words, but I also like more sentences!')
	assert(doc.clean_text == 'I like words and more words but I also like more sentences')
	assert(doc.unique_words == set(['I', 'like', 'words', 'and', 'more', 'but', 'also', 'sentences']))
	assert(doc.counts == {
		'I': 2, 'like': 2, 'words': 2, 'and': 1, 'more': 2, 'but': 1, 'also': 1, 'sentences': 1
	})


