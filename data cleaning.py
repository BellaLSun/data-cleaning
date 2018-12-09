import pandas as pd
import numpy as np
from functools import reduce

df = pd.read_csv('Datasets/BL-Flickr-Images-Book.csv')
to_drop = ['Edition Statement',
           'Corporate Author',
           'Corporate Contributors',
           'Former owner',
           'Engraver',
           'Contributors',
           'Issuance type',
           'Shelfmarks']

df.drop(to_drop, inplace = True, axis = 1)
df.set_index('Identifier', inplace = True)

unwanted_characters = ['[', ',', '-']


def clean_author_names(author):
	author = str(author)

	if author == 'nan':
		return 'NaN'
	# 因为不止一个作者，分成list
	author = author.split(',')

	if len(author) == 1:
		# The method isalpha() checks whether the string consists of alphabetic characters only.
		name = filter(lambda x: x.isalpha(), author[0])
		return reduce(lambda x, y: x + y, name)

	last_name, first_name = author[0], author[1]

	first_name = first_name[:first_name.find('-')] if '-' in first_name else first_name

	if first_name.endswith(('.', '.|')):
		parts = first_name.split('.')

		if len(parts) > 1:
			first_occurence = first_name.find('.')
			final_occurence = first_name.find('.', first_occurence + 1)
			first_name = first_name[:final_occurence]
		else:
			first_name = first_name[:first_name.find('.')]

	last_name = last_name.capitalize()

	return f'{first_name} {last_name}'


df['Author'] = df['Author'].apply(clean_author_names)
