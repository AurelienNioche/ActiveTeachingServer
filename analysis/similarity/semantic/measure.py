import os
import pickle
import uuid
from itertools import combinations

import numpy as np

BKP_FOLDER = os.path.join("data", "word2vec", "pickle")
BKP_FILE = os.path.join(BKP_FOLDER, "semantic_connection.p")

os.makedirs(BKP_FOLDER, exist_ok=True)


def create(word_list, use_nan):

    from . word2vec import word2vec
    sim = word2vec.evaluate_similarity(word_list=word_list, use_nan=use_nan)
    return sim


def _normalize(a):
    return np.interp(a, (np.nanmin(a), np.nanmax(a)), (0, 1))


def _compute(word_list, normalize_similarity=True, verbose=False):

    word_list = [i.lower() for i in word_list]

    sim = create(word_list=word_list, use_nan=normalize_similarity)
    if normalize_similarity:
        sim = _normalize(sim)

    if verbose:
        for i, j in combinations(range(len(word_list)), r=2):
            if i != j:
                a = word_list[i]
                b = word_list[j]
                similarity = sim[i, j]
                print(f"Similarity between {a} and {b} is: {similarity:.2f}")

    return sim


def get(word_list, normalize_similarity=True):

    if os.path.exists(BKP_FILE):

        data, loaded_word_list, loaded_normalize = \
            pickle.load(open(BKP_FILE, 'rb'))
        if loaded_word_list == word_list \
                and loaded_normalize == normalize_similarity:
            return data

    data = _compute(word_list=word_list, normalize_similarity=True)
    pickle.dump(data, word_list, normalize_similarity, open(BKP_FILE, 'wb'))


def demo(word_list=None):

    if not word_list:
        word_list = ['computer', 'myself', 'king']

    _compute(word_list=word_list, verbose=True)
