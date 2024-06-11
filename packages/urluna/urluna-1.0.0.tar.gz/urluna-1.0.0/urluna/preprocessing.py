
from flex import *

class Preprocessing:
    """
    A class for data preprocessing.
    """

    @staticmethod
    def standardize_data(data):
        """
        Standardizes the input data.

        :param data: Input data.
        :return: Standardized data.
        """
        means = [sum(feature) / len(feature) for feature in zip(*data)]
        std_devs = [math.sqrt(sum((x - mean) ** 2 for x in feature) / len(feature)) for mean, feature in zip(means, zip(*data))]
        return [[(x - mean) / std_dev for x, mean, std_dev in zip(sample, means, std_devs)] for sample in data]

    @staticmethod
    def clean_data(data):
        """
        Cleans the input data by removing missing or inconsistent values.

        :param data: Input data.
        :return: Cleaned data.
        """
        cleaned_data = []
        for row in data:
            cleaned_row = [value for value in row if value is not None]
            if len(cleaned_row) == len(row):
                cleaned_data.append(cleaned_row)
        return cleaned_data

    @staticmethod
    def transform_data(data, transformation):
        """
        Transforms the input data using the specified transformation.

        :param data: Input data.
        :param transformation: Transformation function.
        :return: Transformed data.
        """
        return [transformation(row) for row in data]

    @staticmethod
    def prepare_data(data):
        """
        Prepares the input data for machine learning algorithms.

        :param data: Input data.
        :return: Prepared data.
        """
        return Preprocessing.standardize_data(Preprocessing.clean_data(data))