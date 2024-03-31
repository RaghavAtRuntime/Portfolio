from nltk.corpus import words
from itertools import product
import json

def load_dictionary(file_path):
    with open(file_path, 'r') as file:
        return set(word.strip().lower() for word in file)


def is_valid_word(word, grid, visited, i, j):
    if not word:
        return True

    rows, cols = len(grid), len(grid[0])
    if (
            i < 0
            or i >= rows
            or j < 0
            or j >= cols
            or word[0] != grid[i][j]
            or (i, j) in visited
    ):
        return False

    visited.add((i, j))

    for x, y in neighbors(i, j, rows, cols):
        if is_valid_word(word[1:], grid, visited.copy(), x, y):
            return True

    return False


def find_word(word, grid):
    rows, cols = len(grid), len(grid[0])
    for i in range(rows):
        for j in range(cols):
            if is_valid_word(word, grid, set(), i, j):
                return True
    return False


def neighbors(i, j, rows, cols):
    for x, y in product(range(i - 1, i + 2), range(j - 1, j + 2)):
        if 0 <= x < rows and 0 <= y < cols and (x, y) != (i, j):
            yield x, y

def find_possible_words(grid, dictionary):
    possible_words = set()
    for word in dictionary:
        if find_word(word, grid):
            possible_words.add(word)
    return possible_words

def input_to_grid(input_str):
    if len(input_str) != 16:
        raise ValueError("Input must be a 16-character string.")

    return [[input_str[i * 4 + j] for j in range(4)] for i in range(4)]


def find_possible_words_from_input(input_str, dictionary):
    word_grid = input_to_grid(input_str)
    possible_words = find_possible_words(word_grid, dictionary)
    return possible_words

def load_dictionary_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return set(word.lower() for word in data.keys())

# Example usage
if __name__ == "__main__":

    user_input = input("Enter a 16-character string: ")

    json_dictionary_path = 'words_dictionary.json'

    # Load dictionary from JSON
    word_dictionary = load_dictionary_from_json(json_dictionary_path)

    possible_words = find_possible_words_from_input(user_input, word_dictionary)

    print("Possible words:")
    print(sorted(possible_words, key=len, reverse=True))
