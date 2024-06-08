import json
import os
import shutil
from unittest import mock

import dill
from botocore.exceptions import NoCredentialsError
import mongomock

from flowi.experiment_tracking.flavors import SklearnFlavor
from flowi.settings import MONGO_ENDPOINT_URL

import flowi.settings
from flowi.__main__ import main

FLOW_CHART = {
    "offset": {
        "x": -499,
        "y": 318
    },
    "nodes": {
        "0d0fd89e-75a5-4186-8c8f-2d16e04e65e5": {
            "id": "0d0fd89e-75a5-4186-8c8f-2d16e04e65e5",
            "position": {
                "x": 1461,
                "y": 219
            },
            "orientation": 0,
            "type": "Models",
            "ports": {
                "port1": {
                    "id": "port1",
                    "type": "left",
                    "position": {
                        "x": 0,
                        "y": 54
                    }
                },
                "port2": {
                    "id": "port2",
                    "type": "right",
                    "position": {
                        "x": 200,
                        "y": 54
                    }
                }
            },
            "properties": {
                "name": "SVC",
                "function_name": "svc",
                "class": "Classification",
                "description": "C-Support Vector Classification.",
                "attributes": {
                    "C": 1,
                    "break_ties": False,
                    "cache_size": 200,
                    "class_weight": None,
                    "coef0": 0,
                    "decision_function_shape": "ovr",
                    "degree": 3,
                    "gamma": "scale",
                    "kernel": "rbf",
                    "max_iter": -1,
                    "probability": False,
                    "shrinking": True,
                    "target_column": "class",
                    "tol": 0.001
                }
            },
            "size": {
                "width": 200,
                "height": 84
            }
        },
        "13a067af-bc9c-481a-9fb7-e5f31402055c": {
            "id": "13a067af-bc9c-481a-9fb7-e5f31402055c",
            "position": {
                "x": 694,
                "y": 50
            },
            "orientation": 0,
            "type": "Preprocessing",
            "ports": {
                "port1": {
                    "id": "port1",
                    "type": "left",
                    "position": {
                        "x": 0,
                        "y": 42
                    }
                },
                "port2": {
                    "id": "port2",
                    "type": "right",
                    "position": {
                        "x": 282,
                        "y": 42
                    }
                }
            },
            "properties": {
                "name": "Fillna",
                "function_name": "fillna",
                "class": "PreprocessingDataframe",
                "description": "Fill NA/NaN values using the specified method. If both columns and exclude columns are empty, transformation is applied for all columns.",
                "attributes": {
                    "columns": "",
                    "exclude_columns": [
                        "class"
                    ],
                    "fill_value": "0",
                    "missing_values": "nan",
                    "strategy": [
                        "mean",
                        "median"
                    ]
                }
            },
            "size": {
                "width": 282,
                "height": 84
            }
        },
        "46010ec8-09b4-4649-9443-16f519421ed3": {
            "id": "46010ec8-09b4-4649-9443-16f519421ed3",
            "position": {
                "x": 1070,
                "y": 80
            },
            "orientation": 0,
            "type": "Preprocessing",
            "ports": {
                "port1": {
                    "id": "port1",
                    "type": "left",
                    "position": {
                        "x": 0,
                        "y": 42
                    }
                },
                "port2": {
                    "id": "port2",
                    "type": "right",
                    "position": {
                        "x": 282,
                        "y": 42
                    }
                }
            },
            "properties": {
                "name": "StandardScaler",
                "function_name": "standard_scaler",
                "class": "PreprocessingDataframe",
                "description": "Standardize features by removing the mean and scaling to unit variance. If both columns and exclude columns are empty, transformation is applied for all columns.",
                "attributes": {
                    "columns": "",
                    "exclude_columns": [
                        "class"
                    ],
                    "with_mean": True,
                    "with_std": False
                }
            },
            "size": {
                "width": 282,
                "height": 84
            }
        },
        "9ec0927f-5448-4196-b41d-befb21f2e4dd": {
            "id": "9ec0927f-5448-4196-b41d-befb21f2e4dd",
            "position": {
                "x": 1424,
                "y": 110
            },
            "orientation": 0,
            "type": "Models",
            "ports": {
                "port1": {
                    "id": "port1",
                    "type": "left",
                    "position": {
                        "x": 0,
                        "y": 54
                    }
                },
                "port2": {
                    "id": "port2",
                    "type": "right",
                    "position": {
                        "x": 223,
                        "y": 54
                    }
                }
            },
            "properties": {
                "name": "DecisionTree",
                "function_name": "decision_tree",
                "class": "Classification",
                "description": "Train a decision tree classifier.",
                "attributes": {
                    "ccp_alpha": 0,
                    "criterion": [
                        "gini",
                        "entropy"
                    ],
                    "max_depth": 0,
                    "min_impurity_decrease": 0,
                    "min_samples_leaf": 2,
                    "min_samples_split": 4,
                    "min_weight_fraction_leaf": 0,
                    "splitter": "best",
                    "target_column": "class"
                }
            },
            "size": {
                "width": 223,
                "height": 84
            }
        },
        "b0acf050-bfa6-430a-8562-020e885559bc": {
            "id": "b0acf050-bfa6-430a-8562-020e885559bc",
            "position": {
                "x": 409,
                "y": 40
            },
            "orientation": 0,
            "type": "Label",
            "ports": {
                "port1": {
                    "id": "port1",
                    "type": "left",
                    "position": {
                        "x": 0,
                        "y": 42
                    }
                },
                "port2": {
                    "id": "port2",
                    "type": "right",
                    "position": {
                        "x": 229,
                        "y": 42
                    }
                }
            },
            "properties": {
                "name": "LabelEncoder",
                "function_name": "label_encoder",
                "class": "Label",
                "description": "Encode labels to numeric value.",
                "attributes": {
                    "columns": [
                        "class"
                    ],
                    "exclude_columns": [],
                    "is_target_column": "true"
                }
            },
            "size": {
                "width": 229,
                "height": 84
            }
        },
        "b4980acf-670b-4b43-b574-3232c56c37b6": {
            "id": "b4980acf-670b-4b43-b574-3232c56c37b6",
            "position": {
                "x": 139,
                "y": 41
            },
            "orientation": 0,
            "type": "Load",
            "ports": {
                "port1": {
                    "id": "port1",
                    "type": "right",
                    "position": {
                        "x": 200,
                        "y": 42
                    }
                }
            },
            "properties": {
                "name": "LoadFile",
                "function_name": "load_file",
                "class": "LoadLocal",
                "description": "Loads data from path and creates a dataframe.",
                "attributes": {
                    "file_type": "csv",
                    "test_path": "",
                    "test_split": "0.2",
                    "train_path": "iris.csv"
                }
            },
            "size": {
                "width": 200,
                "height": 84
            }
        },
        "b429a773-6ee2-49c5-8b20-552878e10b75": {
            "id": "b429a773-6ee2-49c5-8b20-552878e10b75",
            "position": {
                "x": 1848,
                "y": 150
            },
            "orientation": 0,
            "type": "Metrics",
            "ports": {
                "port1": {
                    "id": "port1",
                    "type": "left",
                    "position": {
                        "x": 0,
                        "y": 54
                    }
                },
                "port2": {
                    "id": "port2",
                    "type": "right",
                    "position": {
                        "x": 200,
                        "y": 54
                    }
                }
            },
            "properties": {
                "name": "Accuracy",
                "function_name": "accuracy",
                "class": "Classification",
                "description": "Compute accuracy score.",
                "attributes": {
                    "normalize": "true"
                }
            },
            "size": {
                "width": 200,
                "height": 84
            }
        },
        "5e2afdce-811b-4965-92dd-570086d53e3c": {
            "id": "5e2afdce-811b-4965-92dd-570086d53e3c",
            "position": {
                "x": 2138,
                "y": 151
            },
            "orientation": 0,
            "type": "Metrics",
            "ports": {
                "port1": {
                    "id": "port1",
                    "type": "left",
                    "position": {
                        "x": 0,
                        "y": 42
                    }
                },
                "port2": {
                    "id": "port2",
                    "type": "right",
                    "position": {
                        "x": 200,
                        "y": 42
                    }
                }
            },
            "properties": {
                "name": "F1Score",
                "function_name": "f1_score",
                "class": "Classification",
                "description": "Compute f1 score.",
                "attributes": {
                    "average": "micro"
                }
            },
            "size": {
                "width": 200,
                "height": 84
            }
        },
        "6877e6f0-8729-41cc-a86d-0d6409d02701": {
            "id": "6877e6f0-8729-41cc-a86d-0d6409d02701",
            "position": {
                "x": 2440,
                "y": 154
            },
            "orientation": 0,
            "type": "Metrics",
            "ports": {
                "port1": {
                    "id": "port1",
                    "type": "left",
                    "position": {
                        "x": 0,
                        "y": 42
                    }
                },
                "port2": {
                    "id": "port2",
                    "type": "right",
                    "position": {
                        "x": 200,
                        "y": 42
                    }
                }
            },
            "properties": {
                "name": "Precision",
                "function_name": "precision",
                "class": "Classification",
                "description": "Compute precision score.",
                "attributes": {
                    "average": "micro"
                }
            },
            "size": {
                "width": 200,
                "height": 84
            }
        },
        "b12749e7-50d8-4ed1-957a-69b5f53727bb": {
            "id": "b12749e7-50d8-4ed1-957a-69b5f53727bb",
            "position": {
                "x": 2698,
                "y": 152
            },
            "orientation": 0,
            "type": "Metrics",
            "ports": {
                "port1": {
                    "id": "port1",
                    "type": "left",
                    "position": {
                        "x": 0,
                        "y": 42
                    }
                },
                "port2": {
                    "id": "port2",
                    "type": "right",
                    "position": {
                        "x": 200,
                        "y": 42
                    }
                }
            },
            "properties": {
                "name": "Recall",
                "function_name": "recall",
                "class": "Classification",
                "description": "Compute recall score.",
                "attributes": {
                    "average": "micro"
                }
            },
            "size": {
                "width": 200,
                "height": 84
            }
        },
        "a60f7df4-a1dc-423e-9c11-a0554a2440d8": {
            "id": "a60f7df4-a1dc-423e-9c11-a0554a2440d8",
            "position": {
                "x": 3010,
                "y": 154
            },
            "orientation": 0,
            "type": "Save",
            "ports": {
                "port1": {
                    "id": "port1",
                    "type": "left",
                    "position": {
                        "x": 0,
                        "y": 42
                    }
                },
                "port2": {
                    "id": "port2",
                    "type": "right",
                    "position": {
                        "x": 200,
                        "y": 42
                    }
                }
            },
            "properties": {
                "name": "SaveFile",
                "function_name": "save_file",
                "class": "SaveLocal",
                "description": "Saves data to a file.",
                "attributes": {
                    "label_column": "class",
                    "save_label_column_only": False,
                    "file_name": "saved.csv",
                    "file_type": "csv"
                }
            },
            "size": {
                "width": 200,
                "height": 84
            }
        }
    },
    "links": {
        "1e16b489-6a1d-4918-91b0-32024b8772a2": {
            "id": "1e16b489-6a1d-4918-91b0-32024b8772a2",
            "from": {
                "nodeId": "13a067af-bc9c-481a-9fb7-e5f31402055c",
                "portId": "port2"
            },
            "to": {
                "nodeId": "46010ec8-09b4-4649-9443-16f519421ed3",
                "portId": "port1"
            }
        },
        "53b83539-987d-4c49-baae-215a80f7d04c": {
            "id": "53b83539-987d-4c49-baae-215a80f7d04c",
            "from": {
                "nodeId": "46010ec8-09b4-4649-9443-16f519421ed3",
                "portId": "port2"
            },
            "to": {
                "nodeId": "0d0fd89e-75a5-4186-8c8f-2d16e04e65e5",
                "portId": "port1"
            }
        },
        "b7ab7044-3057-4998-9486-b88e5a986988": {
            "id": "b7ab7044-3057-4998-9486-b88e5a986988",
            "from": {
                "nodeId": "b4980acf-670b-4b43-b574-3232c56c37b6",
                "portId": "port1"
            },
            "to": {
                "nodeId": "b0acf050-bfa6-430a-8562-020e885559bc",
                "portId": "port1"
            }
        },
        "c148ed7f-4002-4f8b-ba25-f5dc7736153e": {
            "id": "c148ed7f-4002-4f8b-ba25-f5dc7736153e",
            "from": {
                "nodeId": "b0acf050-bfa6-430a-8562-020e885559bc",
                "portId": "port2"
            },
            "to": {
                "nodeId": "13a067af-bc9c-481a-9fb7-e5f31402055c",
                "portId": "port1"
            }
        },
        "eca23b93-ff6c-4ed4-b3d0-7f01f14e7a96": {
            "id": "eca23b93-ff6c-4ed4-b3d0-7f01f14e7a96",
            "from": {
                "nodeId": "46010ec8-09b4-4649-9443-16f519421ed3",
                "portId": "port2"
            },
            "to": {
                "nodeId": "9ec0927f-5448-4196-b41d-befb21f2e4dd",
                "portId": "port1"
            }
        },
        "0321a13c-3858-454b-b76a-f567a6c67a0f": {
            "id": "0321a13c-3858-454b-b76a-f567a6c67a0f",
            "from": {
                "nodeId": "9ec0927f-5448-4196-b41d-befb21f2e4dd",
                "portId": "port2"
            },
            "to": {
                "nodeId": "b429a773-6ee2-49c5-8b20-552878e10b75",
                "portId": "port1"
            }
        },
        "177262c2-4280-4b80-8e84-b85157618049": {
            "id": "177262c2-4280-4b80-8e84-b85157618049",
            "from": {
                "nodeId": "0d0fd89e-75a5-4186-8c8f-2d16e04e65e5",
                "portId": "port2"
            },
            "to": {
                "nodeId": "b429a773-6ee2-49c5-8b20-552878e10b75",
                "portId": "port1"
            }
        },
        "13b0a154-4e9f-4032-8afc-7a4f47aca079": {
            "id": "13b0a154-4e9f-4032-8afc-7a4f47aca079",
            "from": {
                "nodeId": "b429a773-6ee2-49c5-8b20-552878e10b75",
                "portId": "port2"
            },
            "to": {
                "nodeId": "5e2afdce-811b-4965-92dd-570086d53e3c",
                "portId": "port1"
            }
        },
        "1a684810-4a4d-41bc-b2e7-d2371c8f91f8": {
            "id": "1a684810-4a4d-41bc-b2e7-d2371c8f91f8",
            "from": {
                "nodeId": "5e2afdce-811b-4965-92dd-570086d53e3c",
                "portId": "port2"
            },
            "to": {
                "nodeId": "6877e6f0-8729-41cc-a86d-0d6409d02701",
                "portId": "port1"
            }
        },
        "c4a8a341-5173-43fe-828a-fb0f501bb223": {
            "id": "c4a8a341-5173-43fe-828a-fb0f501bb223",
            "from": {
                "nodeId": "6877e6f0-8729-41cc-a86d-0d6409d02701",
                "portId": "port2"
            },
            "to": {
                "nodeId": "b12749e7-50d8-4ed1-957a-69b5f53727bb",
                "portId": "port1"
            }
        },
        "7b4de4dd-6205-46df-8021-50d401b7f75b": {
            "id": "7b4de4dd-6205-46df-8021-50d401b7f75b",
            "from": {
                "nodeId": "b12749e7-50d8-4ed1-957a-69b5f53727bb",
                "portId": "port2"
            },
            "to": {
                "nodeId": "a60f7df4-a1dc-423e-9c11-a0554a2440d8",
                "portId": "port1"
            }
        }
    },
    "selected": {
        "type": "node",
        "id": "13a067af-bc9c-481a-9fb7-e5f31402055c"
    },
    "hovered": {}
}


@mongomock.patch(servers=((MONGO_ENDPOINT_URL, 27017),))
def test_end_to_end_train(mocker):
    mocker.patch.object(flowi.settings, "FLOW_NAME", "End2End Test Flow")
    mocker.patch.object(flowi.settings, "EXPERIMENT_TRACKING", "MLflow")
    mocker.patch("mlflow.register_model")
    mocker.patch("flowi.experiment_tracking._mlflow.MlflowClient.transition_model_version_stage")

    try:
        metric = "accuracy"
        threshold = "0.8"
        main(["train", "--metric", metric, "--threshold", threshold, "--chart", json.dumps(FLOW_CHART)])
    # TODO: Fix airflow write
    except OSError:
        pass
    # TODO: Add boto3 mock
    except NoCredentialsError:
        pass

    os.remove("saved.csv")


PREDICT_SOURCE = {
    "id": "node-load-1",
    "type": "Load",
    "properties": {
        "name": "LoadFile",
        "function_name": "load_file",
        "class": "LoadLocal",
        "attributes": {"train_path": "", "test_path": "iris_pred.csv", "test_split": 0.0, "file_type": "csv"},
    },
}

PREDICT_DESTINY = {
    "id": "node-save-1",
    "type": "Save",
    "properties": {
        "name": "SaveFile",
        "function_name": "save_file",
        "class": "SaveLocal",
        "attributes": {"file_type": "csv", "file_name": "saved.csv", "label_column": "class"},
    },
}


def test_end_to_end_predict(mocker):
    mocker.patch.object(flowi.settings, "FLOW_NAME", "End2End Test Flow")
    mocker.patch.object(flowi.settings, "EXPERIMENT_TRACKING", "MLflow")
    mock_model = mock.Mock()
    mock_model.version.return_value = "1"
    mock_model.run_id.return_value = "run_id"
    mocker.patch("flowi.experiment_tracking._mlflow.MlflowClient.get_model_version", mock_model)
    mocker.patch("flowi.experiment_tracking._mlflow.MlflowClient.download_artifacts")

    shutil.copytree("artifacts/classification", ".", dirs_exist_ok=True)

    with open("model.pkl", "rb") as f:
        model = dill.load(f)
    loaded_model = SklearnFlavor(model=model)
    mocker.patch("flowi.prediction.prediction_batch.load_model_by_version",  return_value=loaded_model)

    try:
        main(["predict", "--source", json.dumps(PREDICT_SOURCE), "--destiny", json.dumps(PREDICT_DESTINY)])
        os.remove("saved.csv")
    # TODO: Add mock to airflow write
    except OSError:
        pass

    os.remove("saved.csv")
    shutil.rmtree("columns")
    shutil.rmtree("drift")
    shutil.rmtree("transformers")
    os.remove("model.pkl")
