#%% Modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%% Exploratory Data Analysis
linkToFolder = "./ml-latest-small/"
def main():
    def average_note(nbUser:int)-> pd.DataFrame:
        '''
        Inputs.
            nbUser: minimum number of users (inclusive) to have given their opinion on the movie. 
                     Set to 0 or 1 to have everyone.
        '''
        ratings = pd.read_csv(linkToFolder + 'ratings.csv')
        movies = pd.read_csv(linkToFolder + 'movies.csv')
        print("Rating data:\n",ratings.head(4))
        print("Movie data:\n", movies.head(4))
        ratings['count'] = ratings.groupby('movieId')['movieId'].transform('count')
        ratings = ratings[ratings['count']>=nbUser]
        avgNote = ratings.groupby('movieId', as_index = False).mean().merge(movies, on = 'movieId')[['title','rating']]
        print("Average note on movies:\n", avgNote.head(8))
        return avgNote

    plt.figure()
    plt.title('Average note of all movies in the DB')
    plt.hist(average_note(5)['rating'],bins = 50)
    plt.show()
    return



if __name__ == '__main__':
    main()