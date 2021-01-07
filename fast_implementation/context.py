#%% Modules
import pandas as pd
from functools import reduce
import time
import csv

#%% Like Threshold
likeThr = 3.2

#%% Aggregation functions
def agg_as_list(series: pd.Series):
    return [series.iloc[k] for k in range(len(series))]

#%% Processing Data : merging ratings and movies into userData variable shared accross all files
# -- change the filePath here
filePath =  "../../ml-latest-small/"
filePathB= '../../../Downloads/'

# -- reading data
ratings = pd.read_csv(filePath + "ratings.csv")
movies = pd.read_csv(filePath + "movies.csv")
links = pd.read_csv(filePath + "links.csv")
tags = pd.read_csv(filePath + "tags.csv")

# -- aggregation
col = ['userId','movieId']
tags = tags.groupby(col, as_index = False).agg(agg_as_list)

# -- merging. keeping keys from rating, but bear in mind that some movies are tagged but do not appear in ratings.csv
userData = pd.merge(ratings, tags, on= ['userId','movieId'], suffixes= ('_rating','_tag'), how='left')

# -- basic tests
assert(type(tags['tag'][0]) == list and type(tags['timestamp'][0]) == list) #tester la correspondance si possible aussi
assert(len(userData) == len(ratings))

# -- creating csv file for good book
books_full=[json.loads(line) for line in open(filePathB + 'goodreads_books_poetry.json','r')]
interact=[json.loads(line) for line in open(filePathB + 'goodreads_interactions_poetry.json','r')]
interactions=[x for x, x in enumerate(interact) if ((x['is_read'] == True) & (x['rating']!=0))]
users_list=[x['user_id'] for x in interactions]
users_list=list(set(users_list))
books_id={books_full[i]['book_id'] : i for i in range(len(books_full))}
users_id={users_list[i] : i for i in range(len(users_list))}

with open('books.csv', 'w', newline='') as file:
    books = csv.writer(file)
    books.writerow(["Id", "Title"])
    for i in books_full:
        books.writerow([books_id[i['book_id']],i['title']])
        
with open('ratingbooks.csv', 'w', newline='') as file:
    ratings = csv.writer(file)
    ratings.writerow(["userId", "bookId", "rating"])
    for i in interactions:
        ratings.writerow([users_id[i['user_id']],books_id[i['book_id']],i['rating']])

books= pd.readcsv("books.csv")