from typing import Dict, Any, Optional, List, Union
import pymongo
import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId


class MongoManager:
    """
    Class to manage MongoDB connection and operations

    Args:
        host (str): Hostname of MongoDB server
        port (int): Port number of MongoDB server
        user_name (str): Username to connect to MongoDB server
        password (str): Password to connect to MongoDB server
        db_name (str): Name of the database to connect to
        default_collection (str): Default collection to connect to

    Example:
        mongo_manager = MongoManager(
            host='localhost',
            port=27017,
            user_name='app',
            password='passw0rd',
            db_name='mlRecommendation',
            default_collection='recommendations'
        )

        data = {"_id": "some_id", "vector": [0.1, 0.2, ....,0.3]}
        mongo_manager.upsert(data)
    """

    def __init__(
        self,
        host,
        port,
        db_name=None,
        user_name=None,
        password=None,
        default_collection=None,
    ):
        self.client = MongoClient(
            host=host,
            port=port,
            username=user_name,
            password=password,
        )
        self.db = self.client[db_name]
        self.collection_name = (
            self.db[default_collection] if default_collection else None
        )

    def get_target_collection(
        self, collection_name: str
    ) -> pymongo.collection.Collection:
        if collection_name:
            return self.db[collection_name]
        else:
            return self.collection_name

    def _create_datapoint(
        self,
        data: Dict,
        id_col_name: str,
        create_timestamp: bool = True,
        timestamp_col_name: str = "created_at",
    ):
        if create_timestamp:
            data[timestamp_col_name] = datetime.datetime.now()
        _id = data.pop(id_col_name)
        return {"_id": _id}, {"$set": data}
    
    def is_doc_exists(self, document_id: str = None, collection_name: str = None) -> bool:
        target_collection = self.get_target_collection(collection_name)
        document = target_collection.find_one({"_id": ObjectId(document_id)})
        return document is not None

    def upsert(
        self,
        data: Union[Dict, List[Dict]],
        collection_name: str = None,
        upsert: bool = True,
        id_col_name: str = "_id",
        create_timestamp: bool = True,
        timestamp_col_name: str = "created_at",
    ):
        target_collection = self.get_target_collection(collection_name)
        if isinstance(data, dict):
            data = [data]
        bulk_operations = []
        for d in data:
            _id, d = self._create_datapoint(
                data=d,
                id_col_name=id_col_name,
                create_timestamp=create_timestamp,
                timestamp_col_name=timestamp_col_name,
            )
            bulk_operations.append(pymongo.UpdateOne(_id, d, upsert=upsert,))
        response = target_collection.bulk_write(bulk_operations)
        return response.acknowledged == True

