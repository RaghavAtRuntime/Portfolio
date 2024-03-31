"""This Python module contains the Code used to run the project.

This file is Copyright (c) 2023 Rohan Bhalla, Raghav Sinha, Grant Bogner, and Bora Celebi.
"""
# Main File
from ui import ui_main
from read_data import import_movies, import_ratings
from graph import Graph

MIN_COMPAT_SCORE = 4.0
MIN_RATING_SCORE = 4.0
RECOMMENDATION_LENGTH = 10

if __name__ == '__main__':
    movie_user_graph = Graph()
    movies_file = "data/movies.csv"
    ratings_file = "data/ratings.csv"

    def load() -> None:
        """Draws loading screen while data is being processed and returned
        """
        import_movies(movies_file, movie_user_graph)
        import_ratings(ratings_file, movie_user_graph)
        movie_user_graph.process_compat_users()
        movie_user_graph.process_movie_recommends(MIN_COMPAT_SCORE, MIN_RATING_SCORE, RECOMMENDATION_LENGTH)

    ui_main(movie_user_graph, load_fn=load)
