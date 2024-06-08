class DummyTransformer(object):
    @staticmethod
    def predict(X):
        return X

    @staticmethod
    def transform(features):
        return features

    @staticmethod
    def inverse_transform(features):
        return features
