import unittest


class DecisionTreeUnitTest(unittest.TestCase):
    def test_decision_tree(self):
        from requests import post
        from os import system
        from pandas import DataFrame, read_json
        from sklearn.datasets import load_iris
        from sklearn.tree import DecisionTreeClassifier

        iris = load_iris()
        input_df = DataFrame(data=iris['data'], columns=iris['feature_names'])
        clf = DecisionTreeClassifier(max_depth=2)
        clf.fit(input_df.values, iris['target'])

        # convert classifier to Docker container
        from sklearn2docker.constructor import Sklearn2Docker
        s2d = Sklearn2Docker(
            classifier=clf,
            feature_names=iris['feature_names'],
            class_names=iris['target_names'].tolist(),
        )
        s2d.save(
            name="classifier",
            tag="iris",
        )

        # run your Docker container as a detached process
        system("docker run -d -p 5000:5000 --name sklearn2docker_unittest classifier:iris && sleep 5")

        # send your training data as a json string
        request = post("http://localhost:5000/predict/split", json=input_df.to_json(orient="split"))
        result = read_json(request.content.decode(), orient="split")
        self.assertEqual(list(result), ['prediction'])
        self.assertGreater(len(result), 0)

        request = post("http://localhost:5000/predict_proba/split", json=input_df.to_json(orient="split"))
        result = read_json(request.content.decode(), orient="split")
        self.assertEqual(list(result), ['setosa', 'versicolor', 'virginica'])
        self.assertGreater(len(result), 0)

        system("docker kill sklearn2docker_unittest")


if __name__ == '__main__':
    unittest.main()
