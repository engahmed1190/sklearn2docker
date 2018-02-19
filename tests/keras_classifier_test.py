

import unittest


class DecisionTreeUnitTest(unittest.TestCase):
    @staticmethod
    def create_model():
        from keras.models import Sequential
        from keras.layers import Dense

        model = Sequential()
        model.add(Dense(12, input_dim=4, activation='relu'))
        model.add(Dense(8, activation='relu'))
        model.add(Dense(3, activation='sigmoid'))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model

    def test_decision_tree(self):
        from keras.wrappers.scikit_learn import KerasClassifier
        from sklearn.datasets import load_iris
        from pandas import DataFrame
        from numpy import array

        iris = load_iris()
        input_df = DataFrame(data=iris['data'], columns=iris['feature_names'])
        model = KerasClassifier(build_fn=self.create_model, epochs=5, verbose=1)
        X, Y = input_df.values, array(iris['target'])
        model.fit(X, Y)




