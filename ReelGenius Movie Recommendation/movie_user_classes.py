""" This Python module contains the User and Movies classes used in this project to represent a user and a movie
in the datasets respectively.

This file is Copyright (c) 2023 Rohan Bhalla, Raghav Sinha, Grant Bogner, and Bora Celebi.
"""
from __future__ import annotations
import doctest
import python_ta


class User:
    """ A class that represents a user

    Instance Attributes
    - user_id:
        The id (unique identifier) for this user.
    - movie_ratings:
        A mapping containing the movies this user has rated. Each key is a movie id and each value is the
        score the user gave.
    - user_compats:
        A mapping containing compatible users. Each key is a user id, and each value is the compatibility score for the
        user
    - recommendations:
        A list of unique recommended movie ids sorted by their recommendation score

    Representation Invariants:
    - self.user_id > 0
    - all({0.5 <= self.movie_ratings[m] <= 5.0 for m in self.movie_ratings})
    - len(self.recommendations) == len(set(self.recommendations))
    """
    user_id: int
    movie_ratings: dict[int, float]
    user_compats: dict[int, float]
    recommendations: list[int]

    def __init__(self, user_id: int) -> None:
        """Initialize this user with the given user_id, and with empty movie_ratings,
        user_compats, and recommendations"""
        self.user_id = user_id
        self.movie_ratings = {}
        self.user_compats = {}
        self.recommendations = []

    def get_movies(self) -> set[int]:
        """Return a set of movie ids for movies this user has rated
        """
        return set(self.movie_ratings)

    def get_rating(self, movie_id: int) -> float:
        """ Return the score this user gave for the movie with id == movie_id

        Preconditions:
        - movie_id in self.movie_ratings
        """
        return self.movie_ratings[movie_id]


class Movie:
    """ A class that represents a movie

    Instance Attributes:
    - movie_id:
        The id (unique identifier) for this movie
    - title:
        The title of this movie
    - user_ratings:
        A mapping containing the users who have rated this movie. Each key is a user id and each value is the score
        given by the user

    Representation Invariants
    - self.movie_id > 0
    - all({0.5 <= self.user_ratings[u] <= 5.0 for u in self.user_ratings})
    """
    movie_id: int
    title: str
    user_ratings: dict[int, float]

    def __init__(self, movie_id: int, title: str) -> None:
        """Initialize the given movie with the given movie_id and title, and with empty user_ratings
        """
        self.movie_id = movie_id
        self.title = title
        self.user_ratings = {}

    def get_users(self) -> list[int]:
        """Return a list of user ids for users that have rated this movie
        """
        return list(self.user_ratings)


if __name__ == '__main__':
    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': ['__future__', 'doctest'],
        'allowed-io': [],
        'max-line-length': 120
    })
