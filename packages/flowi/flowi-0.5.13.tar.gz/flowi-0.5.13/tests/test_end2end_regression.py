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
        "x": -17,
        "y": 13
    },
    "nodes": {
        "08072918-acc7-4004-b448-54a6988c656f": {
            "id": "08072918-acc7-4004-b448-54a6988c656f",
            "position": {
                "x": 933,
                "y": 176
            },
            "orientation": 0,
            "type": "Preprocessing",
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
                        "x": 282,
                        "y": 54
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
                        "Genre",
                        "Popularity"
                    ],
                    "with_mean": True,
                    "with_std": False
                }
            },
            "size": {
                "width": 282,
                "height": 108
            }
        },
        "0b80c66e-b85a-40b0-b0c9-424a54d36c25": {
            "id": "0b80c66e-b85a-40b0-b0c9-424a54d36c25",
            "position": {
                "x": 1267,
                "y": 178
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
                        "x": 335,
                        "y": 54
                    }
                }
            },
            "properties": {
                "name": "RandomForestRegressor",
                "function_name": "random_forest_regressor",
                "class": "Regression",
                "description": "Train a random forest regressor.",
                "attributes": {
                    "bootstrap": True,
                    "max_depth": 0,
                    "min_samples_leaf": 1,
                    "min_samples_split": 2,
                    "min_weight_fraction_leaf": 0,
                    "n_estimators": 10,
                    "oob_score": True,
                    "target_column": "Popularity"
                }
            },
            "size": {
                "width": 335,
                "height": 108
            }
        },
        "1d005a62-8031-468a-bd6f-d4a5512ccaf8": {
            "id": "1d005a62-8031-468a-bd6f-d4a5512ccaf8",
            "position": {
                "x": 594,
                "y": 173
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
                        "Genre",
                        "Popularity"
                    ],
                    "fill_value": 0,
                    "missing_values": "nan",
                    "strategy": [
                        "median"
                    ]
                }
            },
            "size": {
                "width": 282,
                "height": 84
            }
        },
        "4d6ba507-dcc7-466e-b6c2-aca76a8a4949": {
            "id": "4d6ba507-dcc7-466e-b6c2-aca76a8a4949",
            "position": {
                "x": 1735,
                "y": 155
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
                        "x": 282,
                        "y": 54
                    }
                }
            },
            "properties": {
                "name": "MeanSquaredError",
                "function_name": "mean_squared_error",
                "class": "Regression",
                "description": "Compute mean squared error score score.",
                "attributes": {}
            },
            "size": {
                "width": 282,
                "height": 108
            }
        },
        "5001ad7a-3431-485d-933f-c82bdef09824": {
            "id": "5001ad7a-3431-485d-933f-c82bdef09824",
            "position": {
                "x": 2116,
                "y": 177
            },
            "orientation": 0,
            "type": "Save",
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
                "name": "SaveFile",
                "function_name": "save_file",
                "class": "SaveLocal",
                "description": "Saves data to a file.",
                "attributes": {
                    "file_name": "temp-song-popularity.csv",
                    "file_type": "csv",
                    "label_column": "Popularity",
                    "save_label_column_only": "false"
                }
            },
            "size": {
                "width": 200,
                "height": 108
            }
        },
        "505ecb19-5c31-4272-bc26-ddba1a066fae": {
            "id": "505ecb19-5c31-4272-bc26-ddba1a066fae",
            "position": {
                "x": 1730,
                "y": 413
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
                "name": "R2Score",
                "function_name": "r2_score",
                "class": "Regression",
                "description": "Compute R2 (coefficient of determination) regression score function.",
                "attributes": {}
            },
            "size": {
                "width": 200,
                "height": 108
            }
        },
        "581a2bb7-4b8b-45b0-9d0e-b3f6cd42a4e4": {
            "id": "581a2bb7-4b8b-45b0-9d0e-b3f6cd42a4e4",
            "position": {
                "x": 1733,
                "y": 295
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
                        "x": 316,
                        "y": 54
                    }
                }
            },
            "properties": {
                "name": "MeanSquaredLogError",
                "function_name": "mean_squared_log_error",
                "class": "Regression",
                "description": "Compute mean squared log error score score.",
                "attributes": {}
            },
            "size": {
                "width": 316,
                "height": 108
            }
        },
        "91dc65d6-2342-436e-a8a6-57369e9e850f": {
            "id": "91dc65d6-2342-436e-a8a6-57369e9e850f",
            "position": {
                "x": 41,
                "y": 174
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
                    "test_path": "data/song-popularity/test.csv",
                    "test_split": "0.0",
                    "train_path": "data/song-popularity/train.csv"
                }
            },
            "size": {
                "width": 200,
                "height": 84
            }
        },
        "9dcb8c2a-f96f-4d27-8563-bd0228b3fb8d": {
            "id": "9dcb8c2a-f96f-4d27-8563-bd0228b3fb8d",
            "position": {
                "x": 1743,
                "y": 27
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
                        "x": 287,
                        "y": 54
                    }
                }
            },
            "properties": {
                "name": "MeanAbsoluteError",
                "function_name": "mean_absolute_error",
                "class": "Regression",
                "description": "Compute mean absolute error score score.",
                "attributes": {}
            },
            "size": {
                "width": 287,
                "height": 108
            }
        },
        "d047a604-a720-404c-9424-ee67c1f871d9": {
            "id": "d047a604-a720-404c-9424-ee67c1f871d9",
            "position": {
                "x": 322,
                "y": 175
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
                        "Genre"
                    ],
                    "exclude_columns": "",
                    "is_target_column": "false"
                }
            },
            "size": {
                "width": 229,
                "height": 84
            }
        }
    },
    "links": {
        "129339ea-538b-4d62-b461-2b793a5636f9": {
            "id": "129339ea-538b-4d62-b461-2b793a5636f9",
            "from": {
                "nodeId": "1d005a62-8031-468a-bd6f-d4a5512ccaf8",
                "portId": "port2"
            },
            "to": {
                "nodeId": "08072918-acc7-4004-b448-54a6988c656f",
                "portId": "port1"
            }
        },
        "19cdc2f7-0062-4740-93ba-d3403a08b35b": {
            "id": "19cdc2f7-0062-4740-93ba-d3403a08b35b",
            "from": {
                "nodeId": "91dc65d6-2342-436e-a8a6-57369e9e850f",
                "portId": "port1"
            },
            "to": {
                "nodeId": "d047a604-a720-404c-9424-ee67c1f871d9",
                "portId": "port1"
            }
        },
        "207262ed-6d96-4d2b-b9ea-fc65a33454e4": {
            "id": "207262ed-6d96-4d2b-b9ea-fc65a33454e4",
            "from": {
                "nodeId": "0b80c66e-b85a-40b0-b0c9-424a54d36c25",
                "portId": "port2"
            },
            "to": {
                "nodeId": "505ecb19-5c31-4272-bc26-ddba1a066fae",
                "portId": "port1"
            }
        },
        "3016b07e-c145-4ba9-a60b-4a07d985a1b9": {
            "id": "3016b07e-c145-4ba9-a60b-4a07d985a1b9",
            "from": {
                "nodeId": "08072918-acc7-4004-b448-54a6988c656f",
                "portId": "port2"
            },
            "to": {
                "nodeId": "0b80c66e-b85a-40b0-b0c9-424a54d36c25",
                "portId": "port1"
            }
        },
        "4f15be98-b9e2-4e21-b095-0ec811baa30d": {
            "id": "4f15be98-b9e2-4e21-b095-0ec811baa30d",
            "from": {
                "nodeId": "0b80c66e-b85a-40b0-b0c9-424a54d36c25",
                "portId": "port2"
            },
            "to": {
                "nodeId": "4d6ba507-dcc7-466e-b6c2-aca76a8a4949",
                "portId": "port1"
            }
        },
        "5300d94f-436c-4704-9109-a4566985c9cc": {
            "id": "5300d94f-436c-4704-9109-a4566985c9cc",
            "from": {
                "nodeId": "505ecb19-5c31-4272-bc26-ddba1a066fae",
                "portId": "port2"
            },
            "to": {
                "nodeId": "581a2bb7-4b8b-45b0-9d0e-b3f6cd42a4e4",
                "portId": "port2"
            }
        },
        "641ad344-668b-4542-bce0-b785c33573f1": {
            "id": "641ad344-668b-4542-bce0-b785c33573f1",
            "from": {
                "nodeId": "581a2bb7-4b8b-45b0-9d0e-b3f6cd42a4e4",
                "portId": "port2"
            },
            "to": {
                "nodeId": "5001ad7a-3431-485d-933f-c82bdef09824",
                "portId": "port1"
            }
        },
        "8b815fe8-4349-4d9e-a571-ed61395008be": {
            "id": "8b815fe8-4349-4d9e-a571-ed61395008be",
            "from": {
                "nodeId": "0b80c66e-b85a-40b0-b0c9-424a54d36c25",
                "portId": "port2"
            },
            "to": {
                "nodeId": "9dcb8c2a-f96f-4d27-8563-bd0228b3fb8d",
                "portId": "port1"
            }
        },
        "8bab143c-492b-4da7-939b-431133c7be64": {
            "id": "8bab143c-492b-4da7-939b-431133c7be64",
            "from": {
                "nodeId": "0b80c66e-b85a-40b0-b0c9-424a54d36c25",
                "portId": "port2"
            },
            "to": {
                "nodeId": "581a2bb7-4b8b-45b0-9d0e-b3f6cd42a4e4",
                "portId": "port1"
            }
        },
        "8e59a1be-3b1e-4e39-adfa-83c87e5ff3a2": {
            "id": "8e59a1be-3b1e-4e39-adfa-83c87e5ff3a2",
            "from": {
                "nodeId": "4d6ba507-dcc7-466e-b6c2-aca76a8a4949",
                "portId": "port2"
            },
            "to": {
                "nodeId": "5001ad7a-3431-485d-933f-c82bdef09824",
                "portId": "port1"
            }
        },
        "9eb31f09-ecfb-4bec-b8bb-78562d10055a": {
            "id": "9eb31f09-ecfb-4bec-b8bb-78562d10055a",
            "from": {
                "nodeId": "9dcb8c2a-f96f-4d27-8563-bd0228b3fb8d",
                "portId": "port2"
            },
            "to": {
                "nodeId": "5001ad7a-3431-485d-933f-c82bdef09824",
                "portId": "port1"
            }
        },
        "d471373e-eb9c-4bb2-9077-d8ec95d20da6": {
            "id": "d471373e-eb9c-4bb2-9077-d8ec95d20da6",
            "from": {
                "nodeId": "d047a604-a720-404c-9424-ee67c1f871d9",
                "portId": "port2"
            },
            "to": {
                "nodeId": "1d005a62-8031-468a-bd6f-d4a5512ccaf8",
                "portId": "port1"
            }
        }
    },
    "selected": {
        "type": "node",
        "id": "91dc65d6-2342-436e-a8a6-57369e9e850f"
    },
    "hovered": {}
}


@mongomock.patch(servers=((MONGO_ENDPOINT_URL, 27017),))
def test_end_to_end_regression_train(mocker):
    mocker.patch.object(flowi.settings, "FLOW_NAME", "End2End Regression Test Flow")
    mocker.patch.object(flowi.settings, "EXPERIMENT_TRACKING", "MLflow")
    mocker.patch("mlflow.register_model")
    mocker.patch("flowi.experiment_tracking._mlflow.MlflowClient.transition_model_version_stage")

    try:
        metric = "mean_squared_error"
        threshold = "0.8"
        main(["train", "--metric", metric, "--threshold", threshold, "--chart", json.dumps(FLOW_CHART)])
    # TODO: Fix airflow write
    except OSError as e:
        print(f"Error: {e}")
    # TODO: Add boto3 mock
    except NoCredentialsError:
        pass


PREDICT_SOURCE = {
    "id": "node-load-1",
    "type": "Load",
    "properties": {
        "name": "LoadFile",
        "function_name": "load_file",
        "class": "LoadLocal",
        "attributes": {"train_path": "", "test_path": "data/song-popularity/test.csv", "test_split": 0.0, "file_type": "csv"},
    },
}

PREDICT_DESTINY = {
    "id": "node-save-1",
    "type": "Save",
    "properties": {
        "name": "SaveFile",
        "function_name": "save_file",
        "class": "SaveLocal",
        "attributes": {"file_type": "csv", "file_name": "saved.csv", "label_column": "Popularity"},
    },
}


def test_end_to_end_regression_predict(mocker):
    mocker.patch.object(flowi.settings, "FLOW_NAME", "End2End Regression Test Flow")
    mocker.patch.object(flowi.settings, "EXPERIMENT_TRACKING", "MLflow")
    mock_model = mock.Mock()
    mock_model.version.return_value = "1"
    mock_model.run_id.return_value = "run_id"
    mocker.patch("flowi.experiment_tracking._mlflow.MlflowClient.get_model_version", mock_model)
    mocker.patch("flowi.experiment_tracking._mlflow.MlflowClient.download_artifacts")

    shutil.copytree("artifacts/regression", ".", dirs_exist_ok=True)

    with open("model.pkl", "rb") as f:
        model = dill.load(f)
    loaded_model = SklearnFlavor(model=model)
    mocker.patch("flowi.prediction.prediction_batch.load_model_by_version",  return_value=loaded_model)

    try:
        main(["predict", "--source", json.dumps(PREDICT_SOURCE), "--destiny", json.dumps(PREDICT_DESTINY)])
    # TODO: Add mock to airflow write
    except OSError:
        pass

    os.remove("saved.csv")
    shutil.rmtree("columns")
    shutil.rmtree("drift")
    shutil.rmtree("transformers")
    os.remove("model.pkl")
