
from flex import *
from operator import Operator

class MachineLearning:
    """
    A class for machine learning algorithms.
    """

    @staticmethod
    def logistic_regression(X_train, y_train, X_test):
        """
        Logistic regression classifier.

        :param X_train: Training data.
        :param y_train: Training labels.
        :param X_test: Test data.
        :return: Predicted labels.
        """
        def sigmoid(x):
            return 1 / (1 + math.exp(-x))

        def predict(weights, sample):
            z = sum(weight * feature for weight, feature in zip(weights, sample))
            return sigmoid(z)

        def train(X, y, learning_rate=0.01, num_epochs=100):
            num_features = len(X[0])
            weights = [0] * num_features
            for _ in range(num_epochs):
                for features, label in zip(X, y):
                    prediction = predict(weights, features)
                    error = label - prediction
                    for i in range(num_features):
                        weights[i] += learning_rate * error * features[i]
            return weights

        weights = train(X_train, y_train)
        return [1 if predict(weights, sample) >= 0.5 else 0 for sample in X_test]

    @staticmethod
    def k_nearest_neighbors(X_train, y_train, X_test, k=3):
        """
        k-nearest neighbors classifier.

        :param X_train: Training data.
        :param y_train: Training labels.
        :param X_test: Test data.
        :param k: Number of neighbors.
        :return: Predicted labels.
        """
        def euclidean_distance(point1, point2):
            return math.sqrt(sum((x - y) ** 2 for x, y in zip(point1, point2)))

        def most_common_label(labels):
            return max(set(labels), key=labels.count)

        def predict(X_train, y_train, sample, k):
            distances = [(euclidean_distance(sample, train_sample), label) for train_sample, label in zip(X_train, y_train)]
            sorted_distances = sorted(distances, key=lambda x: x[0])
            k_nearest_labels = [label for _, label in sorted_distances[:k]]
            return most_common_label(k_nearest_labels)

        return [predict(X_train, y_train, test_sample, k) for test_sample in X_test]

    @staticmethod
    def naive_bayes_classifier(X_train, y_train, X_test):
        """
        Naive Bayes classifier.

        :param X_train: Training data.
        :param y_train: Training labels.
        :param X_test: Test data.
        :return: Predicted labels.
        """
        def calculate_class_probabilities(X_train, y_train):
            class_probabilities = {}
            total_samples = len(y_train)
            for class_label in set(y_train):
                class_samples = [X_train[i] for i in range(total_samples) if y_train[i] == class_label]
                class_probabilities[class_label] = len(class_samples) / total_samples
            return class_probabilities

        def calculate_feature_statistics(X_train, y_train):
            feature_statistics = {}
            total_samples = len(y_train)
            num_features = len(X_train[0])
            for class_label in set(y_train):
                class_samples = [X_train[i] for i in range(total_samples) if y_train[i] == class_label]
                class_feature_values = list(zip(*class_samples))
                class_feature_stats = [(sum(feature) / len(feature), math.sqrt(sum((x - (sum(feature) / len(feature))) ** 2 for x in feature) / len(feature))) for feature in class_feature_values]
                feature_statistics[class_label] = class_feature_stats
            return feature_statistics

        def calculate_probability(x, mean, stdev):
            exponent = math.exp(-((x - mean) ** 2 / (2 * stdev ** 2)))
            return (1 / (math.sqrt(2 * math.pi) * stdev)) * exponent

        class_probabilities = calculate_class_probabilities(X_train, y_train)
        feature_statistics = calculate_feature_statistics(X_train, y_train)
        predicted_labels = []
        for sample in X_test:
            probabilities = {}
            for class_label, class_prob in class_probabilities.items():
                probabilities[class_label] = class_prob
                for i in range(len(sample)):
                    mean, stdev = feature_statistics[class_label][i]
                    probabilities[class_label] *= calculate_probability(sample[i], mean, stdev)
            predicted_label = max(probabilities, key=probabilities.get)
            predicted_labels.append(predicted_label)
        return predicted_labels

    @staticmethod
    def linear_regression(X_train, y_train, X_test):
        """
        Linear regression.

        :param X_train: Training data.
        :param y_train: Training labels.
        :param X_test: Test data.
        :return: Predicted values.
        """
        def predict(weights, sample):
            return sum(weight * feature for weight, feature in zip(weights, sample))

        def train(X, y):
            num_features = len(X[0])
            weights = [0] * num_features
            transpose_X = Operator.transpose(X)
            X_transpose_X = Operator.multiply_matrices(transpose_X, X)
            inverse_X_transpose_X = Operator.inverse_matrix(X_transpose_X)
            X_transpose_y = Operator.multiply_matrices(transpose_X, [[label] for label in y])
            weights_matrix = Operator.multiply_matrices(inverse_X_transpose_X, X_transpose_y)
            weights = [weight[0] for weight in weights_matrix]
            return weights

        weights = train(X_train, y_train)
        return [predict(weights, sample) for sample in X_test]

    @staticmethod
    def decision_tree(X_train, y_train, X_test, max_depth=None, min_samples_split=2):
        """
        Decision tree classifier with additional parameters for max depth and min samples split.

        :param X_train: Training data.
        :param y_train: Training labels.
        :param X_test: Test data.
        :param max_depth: Maximum depth of the tree.
        :param min_samples_split: Minimum number of samples required to split an internal node.
        :return: Predicted labels.
        """
        class Node:
            def __init__(self, feature_index=None, threshold=None, value=None, left=None, right=None):
                self.feature_index = feature_index
                self.threshold = threshold
                self.value = value
                self.left = left
                self.right = right

        def gini_impurity(labels):
            total_samples = len(labels)
            if total_samples == 0:
                return 0
            probabilities = [labels.count(label) / total_samples for label in set(labels)]
            return 1 - sum(probability ** 2 for probability in probabilities)

        def find_best_split(X, y):
            best_gini = float('inf')
            best_feature_index = None
            best_threshold = None
            for feature_index in range(len(X[0])):
                for sample in X:
                    for threshold in set(sample):
                        left_X, right_X, left_y, right_y = [], [], [], []
                        for sample, label in zip(X, y):
                            if sample[feature_index] < threshold:
                                left_X.append(sample)
                                left_y.append(label)
                            else:
                                right_X.append(sample)
                                right_y.append(label)
                        gini = (len(left_y) / len(y)) * gini_impurity(left_y) + (len(right_y) / len(y)) * gini_impurity(right_y)
                        if gini < best_gini:
                            best_gini = gini
                            best_feature_index = feature_index
                            best_threshold = threshold
            return best_feature_index, best_threshold

        def build_tree(X, y, depth=0):
            if len(set(y)) == 1:
                return Node(value=y[0])
            if max_depth is not None and depth >= max_depth:
                return Node(value=max(set(y), key=y.count))
            if len(y) < min_samples_split:
                return Node(value=max(set(y), key=y.count))
            
            best_feature_index, best_threshold = find_best_split(X, y)
            if best_feature_index is None:
                return Node(value=max(set(y), key=y.count))
            
            left_X, right_X, left_y, right_y = [], [], [], []
            for sample, label in zip(X, y):
                if sample[best_feature_index] < best_threshold:
                    left_X.append(sample)
                    left_y.append(label)
                else:
                    right_X.append(sample)
                    right_y.append(label)
            
            left = build_tree(left_X, left_y, depth + 1)
            right = build_tree(right_X, right_y, depth + 1)
            return Node(feature_index=best_feature_index, threshold=best_threshold, left=left, right=right)

        def predict(node, sample):
            if node.value is not None:
                return node.value
            if sample[node.feature_index] < node.threshold:
                return predict(node.left, sample)
            else:
                return predict(node.right, sample)

        root = build_tree(X_train, y_train)
        return [predict(root, sample) for sample in X_test]

    @staticmethod
    def random_forest(X_train, y_train, X_test, n_trees=100, max_depth=None, min_samples_split=2, max_features=None):
        """
        Random forest classifier.

        :param X_train: Training data.
        :param y_train: Training labels.
        :param X_test: Test data.
        :param n_trees: Number of trees in the random forest.
        :param max_depth: Maximum depth of the trees.
        :param min_samples_split: Minimum number of samples required to split an internal node.
        :param max_features: Number of features to consider when looking for the best split. If None, all features will be considered.
        :return: Predicted labels.
        """
        def bootstrap_sample(X, y):
            n_samples = len(X)
            indices = [random.randint(0, n_samples - 1) for _ in range(n_samples)]
            return [X[i] for i in indices], [y[i] for i in indices]

        def most_common_label(labels):
            return max(set(labels), key=labels.count)

        def build_tree(X, y, depth=0):
            if len(set(y)) == 1 or depth == max_depth:
                return most_common_label(y)

            n_features = len(X[0])
            if max_features and max_features <= n_features:
                feature_indices = random.sample(range(n_features), max_features)
                X = [[sample[i] for i in feature_indices] for sample in X]

            feature_index, threshold = find_best_split(X, y)

            if feature_index is None:
                return most_common_label(y)

            left_X, right_X, left_y, right_y = [], [], [], []
            for sample, label in zip(X, y):
                if sample[feature_index] < threshold:
                    left_X.append(sample)
                    left_y.append(label)
                else:
                    right_X.append(sample)
                    right_y.append(label)

            left_subtree = build_tree(left_X, left_y, depth + 1)
            right_subtree = build_tree(right_X, right_y, depth + 1)

            return {'feature_index': feature_index, 'threshold': threshold,
                    'left': left_subtree, 'right': right_subtree}

        def find_best_split(X, y):
            best_gini = float('inf')
            best_feature_index = None
            best_threshold = None
            for feature_index in range(len(X[0])):
                for sample in X:
                    for threshold in set(sample):
                        left_X, right_X, left_y, right_y = [], [], [], []
                        for sample, label in zip(X, y):
                            if sample[feature_index] < threshold:
                                left_X.append(sample)
                                left_y.append(label)
                            else:
                                right_X.append(sample)
                                right_y.append(label)
                        gini = (len(left_y) / len(y)) * gini_impurity(left_y) + (
                                    len(right_y) / len(y)) * gini_impurity(right_y)
                        if gini < best_gini:
                            best_gini = gini
                            best_feature_index = feature_index
                            best_threshold = threshold
            return best_feature_index, best_threshold

        def gini_impurity(labels):
            total_samples = len(labels)
            if total_samples == 0:
                return 0
            probabilities = [labels.count(label) / total_samples for label in set(labels)]
            return 1 - sum(probability ** 2 for probability in probabilities)

        def predict(tree, sample):
            if isinstance(tree, dict):
                if sample[tree['feature_index']] < tree['threshold']:
                    return predict(tree['left'], sample)
                else:
                    return predict(tree['right'], sample)
            else:
                return tree

        forest = []
        for _ in range(n_trees):
            X_sample, y_sample = bootstrap_sample(X_train, y_train)
            tree = build_tree(X_sample, y_sample)
            forest.append(tree)

        predictions = []
        for sample in X_test:
            tree_predictions = [predict(tree, sample) for tree in forest]
            predictions.append(most_common_label(tree_predictions))

        return predictions