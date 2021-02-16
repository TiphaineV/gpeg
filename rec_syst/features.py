import pandas as pd

class NodeFeatures:
    '''See https://pandas.pydata.org/pandas-docs/stable/reference/groupby.html
    '''  
    Genres = ['Action', 'Adventure', 'Animation', 
        "Children", 'Comedy', 'Crime', 'Documentary', 'Drama',
        'Fantasy', 'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery',
        'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western', '(no genres listed)']
    
    mn = 1891 # small = 1900, heavy = 1891
    mx = 2015 # keep this one
    Years = ["{0} - {1}".format(i, i + 9) for i in range(mn, mx, 10)] #caution

    # -- user

    @staticmethod 
    def user_mean(dfByUser:pd.DataFrame):
        return dfByUser['rating'].agg(np.mean)
    
    @staticmethod
    def user_std(dfByUser:pd.DataFrame):
        return dfByUser['rating'].std(ddof=0)
    
    @staticmethod
    def user_degree(dfByUser:pd.DataFrame):
        return dfByUser.size()
      
    @staticmethod 
    def user_corr_movie(dfByUser:pd.DataFrame):
        # has no interest, but feasible
        return dfByUser[['userId', 'movieId']].corr()['userId'][:, 'movieId']
    
    @staticmethod
    def user_tag(dfByUser:pd.DataFrame):
        return dfByUser['tag'].count().fillna(value=0).astype('uint32')
    
    # -- movie

    @staticmethod 
    def movie_mean(dfByMovie:pd.DataFrame):
        return dfByMovie['rating'].agg(np.mean)
    
    @staticmethod
    def movie_std(dfByMovie: pd.DataFrame):
        return dfByMovie['rating'].std(ddof=0)
    
    @staticmethod
    def movie_degree(dfByMovie: pd.DataFrame):
        return dfByMovie.size()
    
    @staticmethod
    def movie_tag(dfByMovie: pd.DataFrame):
        return dfByMovie['tag'].count().fillna(value=0).astype('uint32')

    @classmethod
    def movie_genre(cls, dfByMovie: pd.DataFrame):
        return dfByMovie[cls.Genres].first()
    
    @classmethod
    def movie_year(cls, dfByMovie: pd.DataFrame):
        return dfByMovie[cls.Years].first()
    
    
    # -- graph

    @staticmethod
    def f():
      pass
    
