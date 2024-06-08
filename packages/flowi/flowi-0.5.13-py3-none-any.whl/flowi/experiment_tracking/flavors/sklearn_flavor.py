class SklearnFlavor(object):
    def __init__(self, model):
        self._model = model

    def predict(self, X):
        return self._model.predict(X)
