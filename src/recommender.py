import logging
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist,squareform

class MovieRecommender():
    """Template class for a Movie Recommender system."""

    def __init__(self):
        """Constructs a MovieRecommender"""
        self.logger = logging.getLogger('reco-cs')
        # ...

    def fill_ratings_mat(self, i, row):
        self.ratings_mat[row['user'], row['movie']] = row['rating']

    def fit(self, ratings_mat):
        """
        Trains the recommender on a given set of ratings.

        Parameters
        ----------
        ratings_mat : nxd array, n = max id of any user, d = max id of any movie

        Returns
        -------
        self : object
            Returns self.
        """
        self.logger.debug("starting fit")
        # self.n = ratings.max()['user']+1
        # self.p = ratings.max()['movie']+1
        self.ratings_mat = ratings_mat
        self.k = ratings_mat.shape[0]//20

        #ratings_array = ratings[ratings.columns[:-1].values].values

        #self.ratings_mat = np.zeros((self.n, self.p))

        #for i, rating in ratings.iterrows():
        #    self.ratings_mat[( rating['user'], rating['movie'] )] = rating['rating']

        self.cosine_dists = squareform(pdist(ratings_mat, 'cosine'))

        #if a user has no ratings data, cosine dist will return a nan. In this case, we assume they are as different as possible, since we cannot predict using those users anyways
        self.cosine_dists = 1 - np.nan_to_num(1 - self.cosine_dists)

        self.similarity_ranks = self.cosine_dists.argsort(axis = 1)

        # ...

        self.logger.debug("finishing fit")
        return(self)

    def pop_pred(self, movie):
        """
        input:int movie id
        output:float predicted rating, based on average rating for that movie
        """
        overall_mean = self.ratings_mat[self.ratings_mat > 0].mean()
        movie_array = self.ratings_mat[:,movie][self.ratings_mat[:,movie] > 0]
        return overall_mean if len(movie_array) == 0 else moviem_array.mean()

    def predict_one(self, user, movie):
        """
        input:int user id, movie id
        output:float predicted rating, based on average ratings by users smilar to the given user.
        """
        neighbors = self.similarity_ranks[user]
        movie_array = self.ratings_mat[neighbors][:,movie]
        movie_array = movie_array[movie_array > 0]
        return movie_array.mean() if len(movie_array) > 0 else self.pop_pred(movie)



    def transform(self, requests):
        """
        Predicts the ratings for a given set of requests.

        Parameters
        ----------
        requests : pandas dataframe, shape = (n_ratings, 2)
                  with columns 'user', 'movie'

        Returns
        -------
        dataframe : a pandas dataframe with columns 'user', 'movie', 'rating'
                    column 'rating' containing the predicted rating
        """
        self.logger.debug("starting predict")
        self.logger.debug("request count: {}".format(requests.shape[0]))

        preds = [self.predict_one(row['user'], row['movie']) for i, row in requests.iterrows()]

        requests['rating'] = preds
        return requests


if __name__ == "__main__":
    logger = logging.getLogger('reco-cs')
    logger.critical('you should use run.py instead')
