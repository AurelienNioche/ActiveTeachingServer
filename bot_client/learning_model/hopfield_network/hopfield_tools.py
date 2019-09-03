import numpy as np


def binarize_item(item, num_neurons):
    """
    Item number to binary and append zeros according to hopfield_network size.
    :param item: int item index
    :return: bin_item binary vector
    """
    question_array = np.array([item])
    bin_item = ((question_array[:, None]
                 & (1 << np.arange(8))) > 0).astype(int)
    bin_item = np.append(bin_item, np.zeros(num_neurons
                                            - bin_item.size))

    print("Item given as pattern:", bin_item)
    return bin_item


def distort_pattern(pattern, proportion):
    """
    Inverts the array in random positions proportional to array size.
    :param pattern: array-like binary vector to distort
    :param proportion: float 0 to 1, 1 being full array inversion
    :return pattern: array-like binary vector with inverted elements
    """

    num_inversions = int(pattern.size * proportion)
    assert proportion != 1
    idx_reassignment = np.random.choice(pattern.size, num_inversions,
                                        replace=False)
    pattern[idx_reassignment] = np.invert(pattern[idx_reassignment] - 2)
    print("\nDistorted pattern (i.e. initial currents)...\n", pattern,
          "\n ...in positions\n", idx_reassignment)
    return pattern


def heaviside_activation(x):
    """Unit step function"""
    return int(x >= 0)


def gaussian_noise(variance):
    # Amplitude-modulated Gaussian noise
    return np.random.normal(loc=0, scale=variance**0.5) * 0.05


# def present_pattern(self, item):
#     kanji = item["kanji"]
#     meaning = item["meaning"]
#
#     self.patterns.append(np.concatenate((kanji, meaning), axis=None))

# flower = {"kanji": np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
#           "meaning": np.array([1, 1, 1, 0, 0, 0, 0, 0, 0, 1])}
#
# leg = {"kanji": np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1]),
#        "meaning": np.array([0, 0, 0, 0, 1, 1, 0, 1, 0, 1])}
#
# eye = {"kanji": np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 0]),
#        "meaning": np.array([0, 0, 0, 0, 1, 0, 1, 1, 1, 1])}
