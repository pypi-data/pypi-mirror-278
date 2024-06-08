import os
from pprint import pprint

import pymongo
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

from flowi.settings import MONGO_ENDPOINT_URL, EXPERIMENT_TRACKING, VERSION, RUN_ID, FLOW_NAME, WORKSPACE


class Mongo(object):
    def __init__(self):
        self._client = self._connect()

        _db = self._client["flowi"]
        self._collection = _db.flowi_training
        self._flows = _db.flows

    @staticmethod
    def _connect() -> pymongo.MongoClient:
        if MONGO_ENDPOINT_URL == "localhost":
            return pymongo.MongoClient(f"mongodb://{MONGO_ENDPOINT_URL}", 27017)
        else:
            _username = os.environ["MONGO_USERNAME"]
            _password = os.environ["MONGO_PASSWORD"]
            uri = f"mongodb+srv://{_username}:{_password}@{MONGO_ENDPOINT_URL}/?retryWrites=true&w=majority"
            return pymongo.MongoClient(uri, server_api=ServerApi('1'))

    def insert(
        self,
        experiment_id: str,
        model_uri: str,
        columns_uri: str,
        drift_detector_uri: str,
        input_transformer_uri: str,
        output_transformer_uri: str,
    ) -> str:
        document = {
            "flow_name": FLOW_NAME,
            "workspace": WORKSPACE,
            "run_id": RUN_ID,
            "version": VERSION,
            "experiment_tracking": EXPERIMENT_TRACKING,
            "experiment_id": experiment_id,
            "model_uri": model_uri,
            "columns_uri": columns_uri,
            "drift_detector_uri": drift_detector_uri,
            "input_transformer_uri": input_transformer_uri,
            "output_transformer_uri": output_transformer_uri,
            "metrics": {},
            "drift": "",
        }
        result = self._collection.insert_one(document)
        return result.inserted_id

    def add_metric(self, mongo_id: str, metric_name: str, value: float):
        self._collection.update_one(
            {"_id": ObjectId(mongo_id)},
            {"$set": {f"metrics.{metric_name}": value}}
        )

    def add_drift(self, mongo_id: str, drift_name: str):
        self._collection.update_one({"_id": ObjectId(mongo_id)}, {"$set": {"drift": drift_name}})

    def stage_model(self, mongo_id: str):
        self._collection.update_one({"_id": ObjectId(mongo_id)}, {"$set": {"staged": "true"}})

    def get_models_by_version(self, run_id: str, version: int or str):
        version = str(version)
        models = []
        cursor = self._collection.find({
            "flow_name": FLOW_NAME,
            "workspace": WORKSPACE,
            "run_id": run_id,
            "version": version
        })
        for document in cursor:
            models.append(document)
        return models

    def show_all(self):
        cursor = self._flows.find({})
        for document in cursor:
            pprint(document)

    def get_staged_model(self, run_id: str):
        staged_model = self._collection.find_one({
            "flow_name": FLOW_NAME,
            "workspace": WORKSPACE,
            "run_id": run_id,
            "staged": "true"
        })
        print(staged_model)
        return staged_model

    def get_deployed_model(self):
        deployed_model = self._collection.find_one({
            "flow_name": FLOW_NAME,
            "workspace": WORKSPACE,
            "deployed": "true"
        })
        print(deployed_model)
        return deployed_model

    def delete(self):
        self._collection.delete_many({"flow_name": FLOW_NAME, "workspace": WORKSPACE})


if __name__ == "__main__":
    mongo = Mongo()
    # mongo.add_drift(mongo_id="613d604afc490d9b0131f3f1", drift_name="kolmogorov_smirnov")
    mongo.show_all()
    # mongo.get_staged_model(flow_name="mnist", run_id="fa02635a-97f3-44ac-99db-d642b4c98b09")
    # mongo.get_deployed_model(flow_name="mnist")
    # mongo.delete(flow_name="MNIST")
