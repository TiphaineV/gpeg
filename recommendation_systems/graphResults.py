#%% Modules
#standard
class Results:
    '''
    Displays different graph properties
    '''
    def __init__(self):
        self.graph = Graph()
        pass
    def prop_movieId(self):
        print('Proportion of ids in range', len(movies['movieId'])/movies['movieId'].max())
        plt.hist(movies['movieId'],bins = 1000)
        plt.show()
        pass

    def users_degree_results(self):
        '''
        Shows the distribution of degrees of the graph
        '''
        graph = self.graph

        plt.figure('Degree distribution, range: infinite')
        graph.display_users_degree_dst(degRange=None)

        plt.figure('Degree distribution, range: 0 - 1000')
        graph.display_users_degree_dst(degRange=(0,1000))

        plt.figure('Degree distribution, range: 0 - 100')
        graph.display_users_degree_dst(degRange=(0,100))

        plt.figure('Degree distribution, range: 0 - 10')
        graph.display_users_degree_dst(degRange=(0,10))
        pass

    def users_AvgRating_results(self):
        '''
        Show the average movie rating of each user
        '''
        graph = self.graph
        plt.figure('Average movie rating of each user')
        graph.display_users_avgRating_dst()
        pass