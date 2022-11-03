import random

random.seed(123)


def set_random_value(array, index):
    array[index] = random.randint(0, 100)
    return array


def assign_random_values(array):

    for index in range(len(array)):
        array = set_random_value(array, index)

    return array

