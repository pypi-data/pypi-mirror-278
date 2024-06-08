# import torch
#
#
# class PytorchFlavor(object):
#     def __init__(self, model):
#         self._model = model
#         self._model.eval()
#
#     def predict(self, X):
#         if not isinstance(X, torch.Tensor):
#             X = torch.tensor(X, dtype=torch.float32)
#
#         with torch.no_grad():
#             y = self._model(X)
#             return y.numpy()
