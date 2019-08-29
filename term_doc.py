"""

Creates a term-document table from a set of documents

"""

import pandas as pd

import document

class TermDoc:

	def __init__(self, documents):

		# create an array of maps where each element
		# in the array is an individual document and
		# each map in the element is a word and count
		self.table = pd.DataFrame([doc.counts for doc in documents])
		# Note: not every individual map will have keys
		# for every term in the table. So there will be many NaNs.
		# NaN means that the term does not occur in the document.
		self.table.fillna(0, inplace=True)

if __name__ == '__main__':

	doc1 = document.Document("Hello World")
	doc2 = document.Document("My name is Shivam")
	doc3 = document.Document("A good greeting is Hello")
	doc4 = document.Document("Shivam is a student")

	term_doc = TermDoc([doc1, doc2, doc3, doc4])
	print(term_doc.table)