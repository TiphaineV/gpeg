'''
Shared data between all files. 
You might have to change the relative link to the dataset.
'''
#%% Modules
import json

#%% Data
# -- relative link to the dataset
filePath =  "../../../../Downloads/"
# -- data shared between files
books=[json.loads(line) for line in open(filePath+'goodreads_books_poetry.json','r')]
reviews=[json.loads(line) for line in open(filePath+'goodreads_reviews_poetry.json','r')]
inte=[json.loads(line) for line in open(filePath+'goodreads_interactions_poetry.json','r')]
interactions=[x for x, x in enumerate(inte) if x['is_read']==False]