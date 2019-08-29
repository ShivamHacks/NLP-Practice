"""

Creates a term-term table from a set of documents

"""

import pandas as pd

import document

class TermTerm:

	"""
	documents: set of Document objects
	window_size: number of words to go in both directions for term-term table
	"""
	def __init__(self, documents, window_size):

		# TODO: algorithm seems to run slowly for even a few small documents

		# loop over the documents and keep track of a map
		# of maps where the key (call it key1) is a term and the
		# value is a map who's key (call it key2) is a term and
		# value is a number that corresponds to how many times
		# the key2 appears in window_size words away from key1

		term_map = {}

		for doc in documents:
			i = 0
			n = len(doc.all_words)
			while i < n:
				start = max(i - window_size, 0) # clip at first word
				end = min(n - 1, i + window_size) # clip end last word
				key1 = doc.all_words[i]

				if key1 not in term_map:
					term_map[key1] = {}
				
				# Note: range(a, b) = [a, ..., b-1]

				# analyze window before i
				for j in range(start, i):
					key2 = doc.all_words[j]
					if key2 not in term_map[key1]:
						term_map[key1][key2] = 1
					else:
						term_map[key1][key2] = term_map[key1][key2] + 1
				
				# analyze window after i
				for j in range(i + 1, end + 1):
					key2 = doc.all_words[j]
					if key2 not in term_map[key1]:
						term_map[key1][key2] = 1
					else:
						term_map[key1][key2] = term_map[key1][key2] + 1

				i = i + 1

		# TODO: explicitly state the index?
		self.table = pd.DataFrame(term_map)
		self.table.fillna(0, inplace=True)

# tests
if __name__ == '__main__':

	doc1 = document.Document("Hello World. This is a complete sentence with Hello in a World")
	doc2 = document.Document("Wow I enjoy saying a Hello but only sometimes with World in a sentence")
	t = TermTerm([doc1, doc2], 4)
