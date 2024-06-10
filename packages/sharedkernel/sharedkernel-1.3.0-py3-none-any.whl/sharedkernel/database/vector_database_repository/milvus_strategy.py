import numpy as np
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType

from .vector_database_strategy import VectorDatabaseStrategy
import uuid


class MilvusStrategy(VectorDatabaseStrategy):
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.collection = None

    def connect(self, host: str = "localhost", port: str = "19530"):
        connections.connect(alias="default", host=host, port=port)
        # Define fields
        fields = [
            FieldSchema(
                name="id", dtype=DataType.VARCHAR, max_length=36, is_primary=True
            ),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=128),
        ]
        schema = CollectionSchema(
            fields, description="Vector collection", enable_dynamic_field=True
        )
        self.collection = Collection(name=self.collection_name, schema=schema)

        if not self.collection.has_index():
             self.collection.create_index(field_name="vector", index_params={"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 128}})

        self.collection.load()

    def insert_vector(self, vector: np.ndarray, metadata: dict) -> str:
        id = str(uuid.uuid4())
        self.collection.insert(data={"id": id, "vector": vector.tolist()})
 
        return id

    def search_vector(self, vector: np.ndarray, top_k: int):
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        results = self.collection.search(
            [vector.tolist()], "vector", search_params, top_k
        )
        return results

    def get_vector_by_id(self, id: str):
        result = self.collection.query(expr=f"id=='{id}'",output_fields=["vector"])
        return result

    def delete_vector(self, id: str):
        self.collection.delete(expr=f"id=='{id}'")
