"""

Positive Pointwise Mutual Information

Improves upon raw word counts for term-doc and term-term tables for word association.
# TODO: can they be used for term-doc tables as well?

Pointwise Mutual Information: Do events x and y co-occur more than if they were independent?

                 P(X,Y)
PMI(X,Y) = log2 --------
                P(X)P(Y)

These values range from -inf to inf, however we do not want negative similarity, so we will
clip values at 0: PPMI(X,Y) = max(0, PMI(X,Y))

Problem with PPMI: It is biased towards infrequent events. Infrequent events will have
low probability, and these values are in the denomintator of the fraction, so they will
result in high values for PMI.

Two solutions:
1) weighting: reduce the context probability by some multiplier
2) k-smoothing: add k to all counts so rare events have higher probabilities


"""

import math

import pandas as pd

"""
table: term-term table stored as a pandas Dataframe object
"""
def ppmi(table, weight=1, smoothing=0):

	# TODO: add weighting
	
	words = list(table.columns)
	contexts = list(table.index.values)

	if smoothing != 0:
		table = table.copy()
		table = table + smoothing

	n = table.values.sum()

	# need to create a new table to store values
	ppmi_table = table.copy().astype('float64')

	for x in words:
		for y in contexts:

			p_xy = table[x][y] / n
			# TODO: p_x and p_y redundantly computed
			p_x = table[x].sum() / n
			p_y = table.loc[y].sum() / n

			# Note: log2(t) < 0 == t < 1
			pmi_pre_log = p_xy / (p_x * p_y)
			if pmi_pre_log < 1:
				ppmi_table[x][y] = 0
			else:
				ppmi_table[x][y] = math.log(pmi_pre_log, 2)

	return ppmi_table

# tests
if __name__ == '__main__':

	table = pd.DataFrame({
		'apricot':     { 'computer': 0, 'data': 0, 'pinch': 1, 'result': 0, 'sugar': 1 },
		'pineapple':   { 'computer': 0, 'data': 0, 'pinch': 1, 'result': 0, 'sugar': 1 },
		'digital':     { 'computer': 2, 'data': 1, 'pinch': 0, 'result': 1, 'sugar': 0 },
		'information': { 'computer': 1, 'data': 6, 'pinch': 0, 'result': 4, 'sugar': 0 }
	})

	print(table)
	ppmi_table = ppmi(table)
	print(ppmi_table.round(2))

	expected = pd.DataFrame({
		'apricot':     { 'computer': 0,    'data': 0,    'pinch': 2.25, 'result': 0,    'sugar': 2.25 },
		'pineapple':   { 'computer': 0,    'data': 0,    'pinch': 2.25, 'result': 0,    'sugar': 2.25 },
		'digital':     { 'computer': 1.66, 'data': 0,    'pinch': 0,    'result': 0,    'sugar': 0    },
		'information': { 'computer': 0,    'data': 0.57, 'pinch': 0,    'result': 0.47, 'sugar': 0    }
	})

	assert(expected.equals(ppmi_table.round(2)))

	ppmi_table = ppmi(table, smoothing=2)
	print(ppmi_table.round(2))

	expected_smoothing = pd.DataFrame({
		'apricot':     { 'computer': 0,    'data': 0,    'pinch': 0.56, 'result': 0,    'sugar': 0.56 },
		'pineapple':   { 'computer': 0,    'data': 0,    'pinch': 0.56, 'result': 0,    'sugar': 0.56 },
		'digital':     { 'computer': 0.62, 'data': 0,    'pinch': 0,    'result': 0,    'sugar': 0    },
		'information': { 'computer': 0,    'data': 0.58, 'pinch': 0,    'result': 0.37, 'sugar': 0    }
	})

	assert(expected_smoothing.equals(ppmi_table.round(2)))

