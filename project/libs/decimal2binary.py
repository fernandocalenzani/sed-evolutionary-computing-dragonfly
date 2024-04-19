import numpy as np


def to_binary(decimal_value):
    bin_array = np.zeros((1, len(decimal_value)))

    for l in range(0, len(decimal_value)):

        bin_array[0][l] = 1 / (1 + np.exp(-decimal_value[l]))

        if bin_array[0][l] >= 0.5:
            bin_array[0][l] = 1
        elif bin_array[0][l] < 0.5:
            bin_array[0][l] = 0

    return bin_array
