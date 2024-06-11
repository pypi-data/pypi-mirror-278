
from flex import *

class Operator:
    """
    A class for performing basic array operations.
    """

    @classmethod
    def add_arrays(cls, array1, array2):
        """
        Adds two arrays element-wise.

        :param array1: First array.
        :param array2: Second array.
        :return: Resultant array after element-wise addition.
        """
        if not isinstance(array1, list) or not isinstance(array2, list):
            raise TypeError("Both parameters must be lists")
        if len(array1) != len(array2) or len(array1[0]) != len(array2[0]):
            raise ValueError("Both arrays must have the same dimensions")

        return [[array1[i][j] + array2[i][j] for j in range(len(array1[0]))] for i in range(len(array1))]

    @classmethod
    def subtract_arrays(cls, array1, array2):
        """
        Subtracts two arrays element-wise.

        :param array1: First array.
        :param array2: Second array.
        :return: Resultant array after element-wise subtraction.
        """
        if not isinstance(array1, list) or not isinstance(array2, list):
            raise TypeError("Both parameters must be lists")
        if len(array1) != len(array2) or len(array1[0]) != len(array2[0]):
            raise ValueError("Both arrays must have the same dimensions")

        return [[array1[i][j] - array2[i][j] for j in range(len(array1[0]))] for i in range(len(array1))]

    @classmethod
    def transpose(cls, matrix):
        """
        Transposes the given matrix.

        :param matrix: Matrix to be transposed.
        :return: Transposed matrix.
        """
        if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
            raise TypeError("Matrix must be a list of lists")
        return [[row[i] for row in matrix] for i in range(len(matrix[0]))]

    @classmethod
    def multiply_matrices(cls, matrix1, matrix2):
        """
        Multiplies two matrices.

        :param matrix1: First matrix.
        :param matrix2: Second matrix.
        :return: Resultant matrix after multiplication.
        """
        if not isinstance(matrix1, list) or not isinstance(matrix2, list):
            raise TypeError("Both parameters must be lists")
        if not all(isinstance(row, list) for row in matrix1) or not all(isinstance(row, list) for row in matrix2):
            raise TypeError("Both parameters must be lists of lists")
        if len(matrix1[0]) != len(matrix2):
            raise ValueError("Number of columns in the first matrix must equal the number of rows in the second matrix")

        result = [[0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix1))]
        for i in range(len(matrix1)):
            for j in range(len(matrix2[0])):
                for k in range(len(matrix2)):
                    result[i][j] += matrix1[i][k] * matrix2[k][j]
        return result

    @classmethod
    def determinant(cls, matrix):
        """
        Calculates the determinant of the given square matrix.

        :param matrix: Square matrix to calculate the determinant.
        :return: Determinant of the matrix.
        """
        if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
            raise TypeError("Matrix must be a list of lists")
        n = len(matrix)
        if n != len(matrix[0]):
            raise ValueError("Matrix must be square")
        if n == 1:
            return matrix[0][0]
        if n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        det = 0
        for i in range(n):
            det += ((-1) ** i) * matrix[0][i] * cls.determinant([row[:i] + row[i + 1:] for row in matrix[1:]])
        return det

    @classmethod
    def inverse_matrix(cls, matrix):
        """
        Calculates the inverse of a matrix.

        :param matrix: Input matrix.
        :return: Inverse of the input matrix.
        """
        if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
            raise TypeError("Matrix must be a list of lists")
        n = len(matrix)
        if n != len(matrix[0]):
            raise ValueError("Matrix must be square")
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for i in range(n):
            row = matrix[i]
            if row[i] == 0:
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        identity[i], identity[j] = identity[j], identity[i]
                        break
            if matrix[i][i] == 0:
                raise ValueError("Matrix is singular")
            scalar = 1 / matrix[i][i]
            matrix[i] = [elem * scalar for elem in matrix[i]]
            identity[i] = [elem * scalar for elem in identity[i]]
            for j in range(n):
                if i != j:
                    scalar = matrix[j][i]
                    matrix[j] = [elem1 - elem2 * scalar for elem1, elem2 in zip(matrix[j], matrix[i])]
                    identity[j] = [elem1 - elem2 * scalar for elem1, elem2 in zip(identity[j], identity[i])]
        return identity
    
    @classmethod
    def hadamard_product(cls, matrix1, matrix2):
        """
        Computes the Hadamard product (element-wise multiplication) of two matrices.

        :param matrix1: First matrix.
        :param matrix2: Second matrix.
        :return: Resultant matrix after element-wise multiplication.
        """
        if not isinstance(matrix1, list) or not isinstance(matrix2, list):
            raise TypeError("Both parameters must be lists")
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Both matrices must have the same dimensions")
        
        return [[matrix1[i][j] * matrix2[i][j] for j in range(len(matrix1[0]))] for i in range(len(matrix1))]

    @classmethod
    def scalar_multiply(cls, matrix, scalar):
        """
        Multiplies a matrix by a scalar value.

        :param matrix: Input matrix.
        :param scalar: Scalar value.
        :return: Resultant matrix after scalar multiplication.
        """
        if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
            raise TypeError("Matrix must be a list of lists")
        if not isinstance(scalar, (int, float)):
            raise TypeError("Scalar must be a number")

        return [[scalar * element for element in row] for row in matrix]
