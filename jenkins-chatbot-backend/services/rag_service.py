import os
import faiss
import numpy as np
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from jenkins_chatbot_backend.config import settings

class RAGService:
    def __init__(self):
        self.index_path = settings.faiss_index_path
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.documents = []
        self.sources = []
        self.chunk_size = 500
        self.chunk_overlap = 50
        self._load_index()

    def _load_index(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            docs_path = self.index_path + "_docs.npy"
            sources_path = self.index_path + "_sources.npy"
            if os.path.exists(docs_path):
                self.documents = np.load(docs_path, allow_pickle=True).tolist()
            if os.path.exists(sources_path):
                self.sources = np.load(sources_path, allow_pickle=True).tolist()
        else:
            self.index = faiss.IndexFlatL2(self.model.get_sentence_embedding_dimension())
            self.documents = []
            self.sources = []

    def index_documents(self, docs: List[Dict[str, Any]]):
        chunks = []
        sources = []
        for doc in docs:
            content = doc["content"]
            source = doc["source"]
            tokens = content.split()
            for i in range(0, len(tokens), self.chunk_size - self.chunk_overlap):
                chunk = " ".join(tokens[i:i+self.chunk_size])
                chunks.append(chunk)
                sources.append(source)
        embeddings = self.model.encode(chunks)
        self.index = faiss.IndexFlatL2(self.model.get_sentence_embedding_dimension())
        self.index.add(np.array(embeddings, dtype=np.float32))
        self.documents = chunks
        self.sources = sources
        faiss.write_index(self.index, self.index_path)
        np.save(self.index_path + "_docs.npy", np.array(self.documents, dtype=object))
        np.save(self.index_path + "_sources.npy", np.array(self.sources, dtype=object))

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if not self.index or not self.documents:
            return []
        query_emb = self.model.encode([query])
        D, I = self.index.search(np.array(query_emb, dtype=np.float32), top_k)
        results = []
        for idx, score in zip(I[0], D[0]):
            if idx < len(self.documents):
                results.append({
                    "content": self.documents[idx],
                    "source": self.sources[idx],
                    "relevance_score": float(score)
                })
        return results
