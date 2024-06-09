from abc import ABC, abstractmethod
import numpy as np

class VectorDatabaseStrategy(ABC):
    @abstractmethod
    def connect(self, **kwargs):
        pass
    @abstractmethod
    def insert_vector(self, vector: np.ndarray, metadata: dict) -> str:
        pass
    
    @abstractmethod
    def search_vector(self, vector: np.ndarray, top_k: int):
        pass
    
    @abstractmethod
    def delete_vector(self, id: str):
        pass
    
    @abstractmethod
    def get_vector_by_id(self, id: str):
        pass
