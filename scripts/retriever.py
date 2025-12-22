# Embeddings + FAISS
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class FaissRetriever:
    def __init__(self, chunks: list[str]):
        self.chunks = chunks
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = self._build_index()

    def _build_index(self):
        embeddings = self.model.encode(self.chunks)
        embeddings = np.array(embeddings).astype("float32")
        faiss.normalize_L2(embeddings)

        index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings)
        return index

    def retrieve(self, query: str, k: int = 3, threshold: float = 0.25) -> list[str]:
        query_embedding = self.model.encode([query]).astype("float32")
        faiss.normalize_L2(query_embedding)

        scores, indices = self.index.search(query_embedding, k)

        results = []
        for idx, score in zip(indices[0], scores[0]):
            if score >= threshold:
                results.append(self.chunks[idx])

        return results
