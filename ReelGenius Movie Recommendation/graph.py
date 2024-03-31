""" This Python module contains the Graph class used to represent the graph used in this project.

This file is Copyright (c) 2023 Rohan Bhalla, Raghav Sinha, Grant Bogner, and Bora Celebi.
"""
import doctest
import python_ta
from movie_user_classes import User, Movie


class Graph:
    """ A class to represent a graph containing User and Movie objects.

    Instance Attributes:
    - _movies:
        A mapping of the movies stored in this graph. Each key is a movie id and each value is a Movie object
    - _users:
        A mapping of the users stored in this graph. Each key is a user id and each value is a User object

    Representation Invariants:
    - all({m == self._movies[m].movie_id for m in self._movies})
    - all({u == self._users[u].user_id for u in self._users})
    """
    _movies: dict[int, Movie]
    _users: dict[int, User]

    def __init__(self) -> None:
        self._movies = {}
        self._users = {}

    def get_all_users(self) -> list[User]:
        """ Returns all users in this graph
        """
        return list(self._users.values())

    def add_movie(self, movie: Movie) -> None:
        """ Adds movie to self._movies. If movie.movie_id is already a key in self._movies, the value stored at that
        key is replaced by movie instead.
        """
        self._movies[movie.movie_id] = movie

    def add_user(self, user: User) -> None:
        """ Adds user to self._users. If user.user_id is already a key in self._users, the value stored at that key
        is replaced by user instead.
        """
        self._users[user.user_id] = user

    def get_movie(self, movie_id: int) -> Movie:
        """ Returns the movie in this graph with id == movie_id

        Preconditions:
        - movie_id in self._movies
        """
        return self._movies[movie_id]

    def get_user(self, user_id: int) -> User:
        """ Returns the user in this graph with id == user_id

        Preconditions:
        - user_id in self._users
        """
        return self._users[user_id]

    def user_exists(self, user_id: int) -> bool:
        """ Returns whether the user with id == user_id is in this graph
        """
        return user_id in self._users

    def process_compat_users(self) -> None:
        """Finds compatible users for each user in graph, calculates their compatability score as outlined in the
        written report, and then updates their user_compats attribute accordingly.
        """
        total_compat_users = 0
        for user in self.get_all_users():
            user_rated_movies = user.get_movies()
            compat_user_ids = self.get_movie_users(user_rated_movies)
            compat_user_ids.remove(user.user_id)
            total_compat_users += len(compat_user_ids)
            self._process_compat_score(user, compat_user_ids)

    def _process_compat_score(self, user: User, compat_user_ids: set[int]) -> None:
        """Compute the compatability scores between user, and all users with ids in compat_user_ids, and update
        user.user_compats accordingly

        Preconditions:
        - graph.user_exists(user.user_id)
        - all({graph.user_exists(id) for id in compat_user_ids})
        """
        for user_id in compat_user_ids:
            user2 = self.get_user(user_id)
            user1_movies = user.get_movies()
            user2_movies = user2.get_movies()
            shared_movies = user1_movies.intersection(user2_movies)
            compat_score_so_far = 0.0
            for movie_id in shared_movies:
                user1_rating = user.get_rating(movie_id)
                user2_rating = user2.get_rating(movie_id)
                compat_score_so_far += abs(user1_rating - user2_rating)
            compat_score_so_far = compat_score_so_far / len(shared_movies)
            compat_score_so_far = 5.0 - compat_score_so_far
            user.user_compats[user_id] = compat_score_so_far

    def process_movie_recommends(self, min_score: float, min_rating: float, recommends_length: int) -> None:
        """Generates a list of recommends_length movie reccommendations for each user in graph, using the strategy
        outlined in the written report and updates their recommended attribute
        accordingly

        Preconditions:
        - min_rating <= 5.0
        - min_score <= 5.0
        - recommends_length > 0
        """
        for user in self.get_all_users():  # loops through all users
            recommendation_list = []
            compat_list = sorted(user.user_compats.items(), key=lambda x: x[1], reverse=True)
            for compat in compat_list:
                uid = compat[0]
                comp_score = compat[1]

                if comp_score < min_score:
                    continue

                compat_user = self.find_or_add_user(uid)
                score_list = _get_recommendation_scores(comp_score, compat_user.movie_ratings, min_rating)
                recommendation_list.extend(score_list)
            sorted_tuples = sorted(recommendation_list, key=lambda x: x[1], reverse=True)
            final_list = [x[0] for x in sorted_tuples]
            unique_list = _remove_duplicates(final_list)
            if len(unique_list) > recommends_length:
                user.recommendations = unique_list[:recommends_length]
            else:
                user.recommendations = unique_list

    def find_or_add_user(self, user_id: int) -> User:
        """Returns the user in graph.users with user_id == id. If such a user does not exist in graph.users,
        the function instead creates a new user with user_id = id, adds it to graph.users, and returns that user

        Preconditions:
        - user_id > 1
        """
        if not self.user_exists(user_id):
            self.add_user(User(user_id))
        return self.get_user(user_id)

    def add_rating(self, user: User, movie_id: int, rating: float) -> None:
        """Adds a rating with movie id and rating to the user's movie_ratings attribute
        and adds a user and its user rating to the movie's user_ratings attribute

        Preconditions:
        - 0.5 <= rating <= 5.0
        """
        user.movie_ratings[movie_id] = rating
        movie = self.get_movie(movie_id)
        movie.user_ratings[user.user_id] = rating

    def get_movie_users(self, movies: set[int]) -> set[int]:
        """Returns a set of ids for users in graph who have a rating for at least one movie whose id is in movies

        Preconditions:
        - all({i in graph._movies for i in movies})
        """
        user_ids_so_far = []
        for movie_id in movies:
            user_ids_so_far.extend(self.get_movie(movie_id).get_users())
        return set(user_ids_so_far)


def _remove_duplicates(lst: list[str]) -> list[str]:
    """Remove duplicates from lst, but keep the first occurrence of each item."""
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def _get_recommendation_scores(comp_score: float, movie_ratings: dict[int, float], min_rating: float)\
        -> list[(int, float)]:
    """
    Given the user rating between a user and its compatible user, and the movie_dict of that compatible user, calculate
    the recommendation scores for each movie in the movie_dict by multiplying the ratings in the dict by the given user
    rating. Return a list of tuples containing the movie ID and its recommendation score.

    Preconditions:
    - 0.5 <= comp_score <= 5.0
    - min_rating <= 5.0
    - all({0.5 <= movie_ratings[m] <= 5.0 for m in movie_ratings})
    """
    rec_list = []
    for k in movie_ratings:
        rating_value = movie_ratings[k]

        if rating_value < min_rating:
            continue

        rec_score = rating_value * comp_score
        rec_list.append((k, rec_score))
    return rec_list


if __name__ == '__main__':
    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': ['movie_user_classes', 'doctest'],
        'allowed-io': [],
        'max-line-length': 120
    })
