import numpy as np
from dummy_lib import assign_random_values


if __name__ == "__main__":
    my_array = np.ones(shape=(10, 1))
    my_array = assign_random_values(my_array)
    assert np.max(my_array) != np.min(my_array)
    print(my_array)


for something in somethings:
    df1 = foo()
    for something_1 in df1.somethings:
        df1_2 = foo(something_1)
