import numpy as np
from .vector_database_strategy import VectorDatabaseStrategy
from .milvus_strategy import MilvusStrategy
from .chroma_startegy import ChromaStrategy
from sharedkernel.enum.vector_database_type import VectorDatabaseType

class VectorRepository:
    def __init__(self, database_type: VectorDatabaseType, collection_name: str, **connection_params):
        self.strategy = self._get_strategy(database_type, collection_name)
        self.strategy.connect(**connection_params)
    
    def _get_strategy(self, database_type: VectorDatabaseType, collection_name: str) -> VectorDatabaseStrategy:
        if database_type == VectorDatabaseType.MILVUS:
            return MilvusStrategy(collection_name)
        else:
            return ChromaStrategy(collection_name)
    
    def add_vector(self, vector: np.ndarray, metadata: dict) -> str:
        return self.strategy.insert_vector(vector, metadata)
    
    def find_similar_vectors(self, vector: np.ndarray, top_k: int):
        return self.strategy.search_vector(vector, top_k)
    
    def remove_vector(self, id: str):
        self.strategy.delete_vector(id)

    def get_vector_by_id(self, id: str):
       return self.strategy.get_vector_by_id(id)