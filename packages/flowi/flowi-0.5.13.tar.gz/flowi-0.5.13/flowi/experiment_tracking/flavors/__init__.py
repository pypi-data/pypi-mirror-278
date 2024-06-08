from flowi.experiment_tracking.flavors.sklearn_flavor import SklearnFlavor
# from flowi.experiment_tracking.flavors.pytorch_flavor import PytorchFlavor

MODEL_FLAVORS = [
    "keras",
    "tensorflow",
    "pytorch",
    "pytorch_lighting",
    "lightning",
    "sklearn",
]

__all__ = [
    SklearnFlavor,
    # PytorchFlavor
]
