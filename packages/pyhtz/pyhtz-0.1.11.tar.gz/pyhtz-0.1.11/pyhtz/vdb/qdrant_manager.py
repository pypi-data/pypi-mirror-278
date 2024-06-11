import itertools
from typing import Any, List, Dict, Union
import requests
from qdrant_client.models import Distance, VectorParams, UpsertOperation, PointsList, PointStruct 
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse, ResponseHandlingException
import pandas as pd
import retry
import time


class QdrantManager(QdrantClient):
    METRIC_MAP = {
        "cosine": Distance.COSINE,
        "euclidean": Distance.EUCLID,
        "dot": Distance.DOT,
    }
    """
    Class to manage Qdrant connection and operations
    Can manage multiple collections
    """

    def __init__(self,**kwargs):
        super(QdrantManager, self).__init__(**kwargs)

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)
    
    def validate_metrics(self, distance_metric):
        if distance_metric not in self.METRIC_MAP.keys():
            raise ValueError(
                f"Invalid distance metric - {distance_metric}. Supported metrics are {self.METRIC_MAP.keys()}"
            )

    def add_collection(
        self,
        collection_name: str,
        dim_size: int = None,
        distance_metric: str = None,
        index_field: str = None,
        if_collection_exists: str = 'raise',
    ):
        self.validate_metrics(distance_metric)
        re_create_collection = True if if_collection_exists == "re-create" else False
        try:
            collection_exists = self._client.collection_exists(collection_name)
            if collection_exists and not re_create_collection:
                    print("Collection already exists, set if_collection_exists='re-create' to recreate the collection")
                    raise ValueError("Collection already exists")
            
            elif collection_exists and re_create_collection or not collection_exists: 
                response = self._recreate_collection(
                    collection_name=collection_name,
                    dim_size=dim_size,
                    metric=self.METRIC_MAP[distance_metric],
                )
                
                if index_field:
                    self._client.create_payload_index(
                        collection_name=collection_name,
                        field_name=index_field,
                        field_schema="keyword",
                    ) 
                return response
                
        except ResponseHandlingException:
            print("Connection refused - Check if Qdrant server is running")            

    @retry.retry(tries=3, delay=5, exceptions=Exception)
    def check_health(self, _client_path):
        response = requests.get(_client_path)
        if response.status_code == 200:
            return True
        else:
            return False

    def _recreate_collection(
        self, collection_name, dim_size: int = None, metric: str = None
    ):
        self._client.delete_collection(collection_name)
        response = self._client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=dim_size, distance=metric),
        )
        return response

    def get_existing_vdb_ids(self) -> List[str]:
        limit = max(self._client.count(collection_name=self.collection_name).count, 1)
        results, _ = self._client.scroll(
            collection_name=self.collection_name, limit=limit
        )
        results = list(set([res.id for res in results]))
        return results

    def _create_points_from_pandas(
        self,
        df: pd.DataFrame,
        point_id_col: str = "_id",
        vector_col: str = "vector",
        payload_cols: list = None,
    ) -> List[PointStruct]:
        """
        Create vector points from pandas DataFrame
        """
        points = [
            PointStruct(
                id=row[df.columns.get_loc(point_id_col)],
                vector=(
                    row[df.columns.get_loc(vector_col)].tolist()
                    if not isinstance(row[df.columns.get_loc(vector_col)], list)
                    else row[df.columns.get_loc(vector_col)]
                ),
                payload={col:row[df.columns.get_loc(col)] for col in payload_cols} if payload_cols else None,
            )
            for row in df.itertuples(index=False)
        ]
        return points

    @staticmethod
    def batches(df, batch_size):
        """
        Yield batches of DataFrames from the input DataFrame.

        :param df: The input DataFrame.
        :param batch_size: The number of rows to include in each batch.
        :yield: A batch of DataFrames.
        """
        for i in range(0, len(df), batch_size):
            yield df.iloc[i:i+batch_size]



    def upsert_batch(
        self,
        collection_name: str,
        data: pd.DataFrame,
        point_id_col: str = "_id",
        vector_col: str = "vector",
        payload_cols: list = None,
        batch_size: int = 10,
        wait: bool = False,
    ):
        """
        Upsert batch of data to Qdrant, vector is expected to be in the column named 'vector'
        Args:
            collection_name (str): Name of the collection
            data (Union[pd.DataFrame, List[Dict[str, Any]]]): Data to upsert
            point_id_col (str): Column name of the point id
            text_col (str): Column name of the text
            payload_cols (list): List of column names for payload
            batch_size (int): Batch size for upsert

        Example:
            data = {
                "article_id": ["1", "2", "3"],
                "article_body": ["Hello, World!", "Hello, Universe!", "Hello, Galaxy!"],
                "article_name": ["World", "Universe", "Galaxy"],
                "article_url": ["http://world.com", "http://universe.com", "http://galaxy.com"]
            }
            df = pd.DataFrame(data)
            qdrant_manager.upsert_batch(
                data, 
                point_id_col="article_id", 
                text_col="article_body", 
                payload_cols=["article_name", "article_url"]
            )

        """
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)
        for batch in self.batches(data, batch_size=batch_size):
            _points = self._create_points_from_pandas(
                df=batch, point_id_col=point_id_col, vector_col=vector_col,payload_cols=payload_cols
            )
            self._client.batch_update_points(
            collection_name=collection_name,
            update_operations=[
                UpsertOperation(
                    upsert=PointsList(points=_points)
                    )
                    ],
            wait=wait,
            )
            

    def upsert(self, collection_name: str, id: str, vector: list, payload: dict = None):
        """
        Upsert single point to Qdrant
        Args:
            collection_name (str): Name of the collection
            id (str): Id of the point
            vector (list): Vector of the point
            payload (dict): Payload of the point

        Example:
            qdrant_manager.upsert(
                collection_name="articles", 
                id="4", vector=[0.1, 0.2, 0.3], 
                payload={"article_name": "Planet", "article_url": "http://planet.com"}
            )
        """
        point = PointStruct(id=id, vector=vector, payload=payload)
        response = self._client.upsert(collection_name=collection_name, points=[point])
        return response.status.value == 'completed'