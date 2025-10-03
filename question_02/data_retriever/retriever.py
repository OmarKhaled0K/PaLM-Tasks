from typing import List, Dict, Optional
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS
from langchain.retrievers import EnsembleRetriever
from langchain_openai import OpenAIEmbeddings
from langchain_core.embeddings import Embeddings
import numpy as np
from dotenv import load_dotenv
load_dotenv()  

class NormalizedEmbeddings(Embeddings):
    def __init__(self, base: Embeddings):
        self.base = base

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        raw = self.base.embed_documents(texts)
        return [self._normalize(v) for v in raw]

    def embed_query(self, text: str) -> List[float]:
        raw = self.base.embed_query(text)
        return self._normalize(raw)

    def _normalize(self, v: List[float]) -> List[float]:
        arr = np.array(v, dtype=float)
        norm = np.linalg.norm(arr)
        return (arr / norm).tolist() if norm > 0 else arr.tolist()


class SimpleRetriever:
    def __init__(self, snippets: List[str],  embedding_model=None):
        self.embedding_model = embedding_model or OpenAIEmbeddings()

        self.bm25 = BM25Retriever.from_texts(
            snippets, metadatas=[{"source": "bm25"}] * len(snippets)
        )

        self.snippets = snippets

    def _make_faiss(self, metric: str, k: int):
        emb = self.embedding_model
        if metric == "cosine":
            emb = NormalizedEmbeddings(self.embedding_model)
        else:
            emb = self.embedding_model

        vs = FAISS.from_texts(
            self.snippets, emb, metadatas=[{"source": "faiss"}] * len(self.snippets)
        )

        return vs.as_retriever(search_kwargs={"k": k})

    def retrieve(self,query: str,retriever_type: str = "faiss",  top_k: int = 3,metric: str = "cosine", weights: Optional[List[float]] = None):
        if retriever_type == "bm25":
            self.bm25.k = top_k
            chunks = self.bm25.invoke(query)
            return chunks[0].page_content if chunks else None, chunks

        elif retriever_type == "faiss":
            retr = self._make_faiss(metric, top_k)
            chunks = retr.invoke(query)
            return chunks[0].page_content if chunks else None, chunks

        elif retriever_type == "hybrid":
            faiss_retr = self._make_faiss(metric, top_k)
            self.bm25.k = top_k

            retrievers = [self.bm25, faiss_retr]
            if not weights:
                weights = [0.5, 0.5]

            ensemble = EnsembleRetriever(retrievers=retrievers, weights=weights)
            chunks = ensemble.invoke(query)
            return chunks[0].page_content if chunks else None, chunks

        else:
            raise ValueError("retriever_type must be 'bm25', 'faiss', or 'hybrid'")

