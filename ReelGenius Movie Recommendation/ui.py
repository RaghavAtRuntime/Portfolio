"""This Python module contains the main functions/pages for the graphical user interface.

This file is Copyright (c) 2023 Rohan Bhalla, Raghav Sinha, Grant Bogner, and Bora Celebi.
"""
import tkinter as tk
from tkinter import ttk
from random import randint

import doctest
import python_ta

from graph import Graph
from movie_user_classes import User


def ui_main(graph: Graph, load_fn: lambda _: _) -> None:
    """ Starts UI and calls load_fn to load data for display
    """
    root = tk.Tk()

    # Loading page
    loading_page = LoadingPage(root)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(1, weight=1)
    root.resizable(False, False)
    root.title("Loading...")
    root.update()
    load_fn()
    loading_page.destroy()

    # User page
    user = graph.get_user(randint(1, len(graph.get_all_users())-1))
    UserPage(root, graph, user)
    root.title("ReelGenius")
    root.mainloop()


class LoadingPage(tk.Frame):
    """ Page with loading progress indicator
    """

    def __init__(self, root: tk.Tk) -> None:
        tk.Frame.__init__(self, root, width=100)


class UserPage(tk.Frame):
    """ Page displaying the graph data for a user
    """
    _root: tk.Tk
    _graph: Graph
    _user: User
    _search_entry: ttk.Entry

    def __init__(self, root: tk.Tk, graph: Graph, user: User) -> None:
        self._root = root
        self._graph = graph
        self._user = user

        tk.Frame.__init__(self, root, padx=10, pady=10)

        # Row 0
        ttk.Label(self, text="ReelGenius", font=(None, 15)).grid(row=0, column=0)
        self._search_entry = ttk.Entry(self)
        self._search_entry.grid(row=0, column=1)
        ttk.Button(self, command=self._search, text="Search User").grid(row=0, column=2)

        # User id
        ttk.Label(self, text=f"User {user.user_id}", font=(None, 20), padding=10).grid(row=1, column=0)

        # Counts
        count_str = f"Recommendations: {len(user.recommendations)}" \
                    f",  My Ratings: {len(user.movie_ratings)}" \
                    f",  Compatible Users: {len(user.user_compats)}"
        ttk.Label(self, text=count_str, font=(None, 12)).grid(row=2, column=0, columnspan=3)

        # Tabs
        notebook = ttk.Notebook(self)
        notebook.add(RecommendationsFrame(notebook, graph, user), text="Recommendations")
        notebook.add(MyRatingsFrame(notebook, graph, user), text="My Ratings")
        notebook.add(CompatibleUsersFrame(notebook, user, self._user_link), text="Compatible Users")
        notebook.grid(row=3, column=0, columnspan=3, sticky='nwes')

        self.pack(fill=tk.BOTH, expand=True)

    def _user_link(self, user_id: int) -> None:
        """ Reloads the page with the data for a different user
        """
        if self._graph.user_exists(user_id):
            self._user = self._graph.get_user(user_id)
            self._reload()

    def _search(self) -> None:
        """ Parses the search bar and links to the user id
        """
        entry_str = self._search_entry.get()
        self._search_entry.delete(0, tk.END)
        if entry_str.isdigit():
            new_user_id = int(entry_str)
            self._user_link(new_user_id)

    def _reload(self) -> None:
        """ Reloads the page
        """
        self.destroy()
        self._root.update()
        self.__init__(self._root, self._graph, self._user)


class RecommendationsFrame(ttk.Frame):
    """ Frame displaying list of movie recommendations
    """

    def __init__(self, notebook: ttk.Notebook, graph: Graph, user: User) -> None:
        ttk.Frame.__init__(self, notebook)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient='vertical')
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        # Treeview
        tree = ttk.Treeview(self, column=("c1", "c2"), show='headings', height=10)
        tree.column("# 1", anchor=tk.CENTER)
        tree.heading("# 1", text="Title")
        tree.column("# 2", anchor=tk.CENTER)
        tree.heading("# 2", text="Rank")

        for i, movie_id in enumerate(user.recommendations):
            movie = graph.get_movie(movie_id)
            cell_1 = movie.title
            cell_2 = str(i + 1)
            tree.insert('', 'end', text=cell_1, values=(cell_1, cell_2))
        tree.pack()

        tree.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)


class MyRatingsFrame(ttk.Frame):
    """ Frame displaying list of movie ratings
    """

    def __init__(self, notebook: ttk.Notebook, graph: Graph, user: User) -> None:
        ttk.Frame.__init__(self, notebook)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient='vertical')
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        # Treeview
        tree = ttk.Treeview(self, column=("c1", "c2"), show='headings', height=10)
        tree.column("# 1", anchor=tk.CENTER)
        tree.heading("# 1", text="Title")
        tree.column("# 2", anchor=tk.CENTER)
        tree.heading("# 2", text="Rating")

        for movie_id, rating in user.movie_ratings.items():
            movie = graph.get_movie(movie_id)
            cell_1 = movie.title
            cell_2 = str(rating)
            tree.insert('', 'end', text=cell_1, values=(cell_1, cell_2))
        tree.pack()

        tree.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)


class CompatibleUsersFrame(ttk.Frame):
    """ Frame displaying list of compatible users
    """

    def __init__(self, notebook: ttk.Notebook, user: User, user_link_fn: lambda _: None) -> None:
        ttk.Frame.__init__(self, notebook)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient='vertical')
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        # Treeview
        tree = ttk.Treeview(self, column=("c1", "c2"), show='headings', height=10)
        tree.column("# 1", anchor=tk.CENTER)
        tree.heading("# 1", text="User")
        tree.column("# 2", anchor=tk.CENTER)
        tree.heading("# 2", text="Score")
        tree.tag_configure('link', foreground='blue', font=(None, 13, 'underline'))

        for user_id, score in sorted(user.user_compats.items(), key=lambda x: x[1], reverse=True):
            cell_1 = 'User ' + str(user_id)
            cell_2 = f"{score:.2f}"
            tree.insert('', 'end', tags=[user_id, 'link'], text=cell_1, values=(cell_1, cell_2))
        tree.pack()

        # Clickable user links
        def tree_press(_: tk.Event) -> None:
            input_id = tree.selection()
            selected_user_id = int(tree.item(input_id, 'tags')[0])
            user_link_fn(selected_user_id)

        tree.bind("<Double-1>", tree_press)

        tree.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)


if __name__ == '__main__':
    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': ['tkinter', 'movie_user_classes', 'graph', 'doctest', 'random'],
        'allowed-io': [],
        'max-line-length': 120
    })
