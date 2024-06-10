import chromadb
import numpy as np
from chromadb.config import Settings
from .vector_database_strategy import VectorDatabaseStrategy
import uuid


class ChromaStrategy(VectorDatabaseStrategy):
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.collection = None

    def connect(self, host: str = "localhost", port: int = 8000):
        client = chromadb.Client(
            Settings(
                chroma_api_impl="rest",
                chroma_server_host=host,
                chroma_server_http_port=port,
            )
        )
        self.collection = client.get_or_create_collection(self.collection_name)

    def insert_vector(self, vector: np.ndarray, metadata: dict) -> str:
        id = str(uuid.uuid4())
        self.collection.upsert(ids=id, embeddings=vector.tolist(), metadatas=[metadata])

        return id

    def search_vector(self, vector: np.ndarray, top_k: int):
        results = self.collection.query(vectors=[vector.tolist()], n_results=top_k)
        return results

    def get_vector_by_id(self, id: str):
        result = self.collection.get(ids=id)

        return result

    def delete_vector(self, id: str):
        self.collection.delete(ids=id)
