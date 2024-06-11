
import random
import math


class Flex:
    """
    A class for performing various flexible array operations.
    """

    @classmethod
    def fill_array(cls, value, num_rows, num_cols):
        """
        Generates a 2D array filled with the specified value.

        :param value: Value to fill the array with.
        :param num_rows: Number of rows in the array.
        :param num_cols: Number of columns in the array.
        :return: 2D array filled with the value.
        """
        if not isinstance(value, int) or not isinstance(num_rows, int) or not isinstance(num_cols, int):
            raise TypeError("All parameters must be integers")
        if num_rows < 0 or num_cols < 0:
            raise ValueError("Number of rows and columns must be non-negative")
        return [[value] * num_cols for _ in range(num_rows)]

    @classmethod
    def sorted_random_array(cls, min_value, max_value, num_rows, num_cols):
        """
        Generates a 2D array filled with random values sorted in ascending order.

        :param min_value: Minimum value for random generation.
        :param max_value: Maximum value for random generation.
        :param num_rows: Number of rows in the array.
        :param num_cols: Number of columns in the array.
        :return: 2D array filled with random values sorted in ascending order.
        """
        if not isinstance(min_value, int) or not isinstance(max_value, int) or not isinstance(num_rows, int) or not isinstance(num_cols, int):
            raise TypeError("All parameters must be integers")
        if min_value > max_value:
            raise ValueError("Minimum value must be less than or equal to Maximum value")
        random_list = [random.randint(min_value, max_value) for _ in range(num_rows * num_cols)]
        random_list.sort()
        return [random_list[i * num_cols: (i + 1) * num_cols] for i in range(num_rows)]

    @classmethod
    def random_array(cls, min_value, max_value, num_rows, num_cols):
        """
        Generates a 2D array filled with random values.

        :param min_value: Minimum value for random generation.
        :param max_value: Maximum value for random generation.
        :param num_rows: Number of rows in the array.
        :param num_cols: Number of columns in the array.
        :return: 2D array filled with random values.
        """
        if not isinstance(min_value, int) or not isinstance(max_value, int) or not isinstance(num_rows, int) or not isinstance(num_cols, int):
            raise TypeError("All parameters must be integers")
        if min_value > max_value:
            raise ValueError("Minimum value must be less than or equal to Maximum value")
        return [[random.randint(min_value, max_value) for _ in range(num_cols)] for _ in range(num_rows)]

    @classmethod
    def range_array(cls, start, stop=None, step=1):
        """
        Generates an array containing evenly spaced values within a given range.

        :param start: Start of the range.
        :param stop: End of the range.
        :param step: Step between each value.
        :return: Array containing evenly spaced values within the given range.
        """
        if stop is None:
            start, stop = 0, start

        if not isinstance(start, int) or not isinstance(stop, int) or not isinstance(step, int):
            raise TypeError("Start, stop, and step must be integers")

        if step == 0:
            raise ValueError("Step must not be zero")

        result = list(range(start, stop, step))
        return [result]

    @classmethod
    def zeros_array(cls, num_rows, num_cols):
        """
        Generates a 2D array filled with zeros.

        :param num_rows: Number of rows in the array.
        :param num_cols: Number of columns in the array.
        :return: 2D array filled with zeros.
        """
        return cls.fill_array(0, num_rows, num_cols)

    @classmethod
    def ones_array(cls, num_rows, num_cols):
        """
        Generates a 2D array filled with ones.

        :param num_rows: Number of rows in the array.
        :param num_cols: Number of columns in the array.
        :return: 2D array filled with ones.
        """
        return cls.fill_array(1, num_rows, num_cols)
    
    @classmethod
    def identity_matrix(cls, size):
        """
        Generates an identity matrix of given size.

        :param size: Size of the identity matrix.
        :return: Identity matrix.
        """
        if not isinstance(size, int) or size < 0:
            raise TypeError("Size must be a non-negative integer")
        return [[1 if i == j else 0 for j in range(size)] for i in range(size)]

    @classmethod
    def diagonal_matrix(cls, diagonal):
        """
        Generates a diagonal matrix with the given diagonal elements.

        :param diagonal: List of diagonal elements.
        :return: Diagonal matrix.
        """
        if not isinstance(diagonal, list):
            raise TypeError("Diagonal must be a list of numbers")
        size = len(diagonal)
        return [[diagonal[i] if i == j else 0 for j in range(size)] for i in range(size)]
