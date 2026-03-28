import numpy as np
import faiss
import re
from rank_bm25 import BM25Okapi
from rag.models import Metadata,semantic_metadata
from sentence_transformers import SentenceTransformer

class C_index():
    def __init__(self,value):
        value.embed_model = SentenceTransformer("all-MiniLM-L6-v2")

    def tokenize(self, text):
        return re.findall(r"\w+", text.lower())

    def create_faiss_index(self, value) -> Metadata:
        value.embeddings = value.embed_model.encode(value.chunks)
        for text, emb in zip(value.chunks, value.embeddings):
            value.records.append(semantic_metadata(**{"text": text, "embedding": emb}))
            print(value.records)
        value.vectors = np.array([r.embedding for r in value.records]).astype("float32")
        dim = value.vectors.shape[1]
        value.index = faiss.IndexFlatL2(dim)
        value.index.add(value.vectors)
        print(f"[INFO] FAISS index created with {len(value.vectors)} chunks")
        return value


    def create_bm25_index(self, value) -> Metadata:
        # -------- Sparse (BM25) --------
        tokenized_corpus = [self.tokenize(chunk) for chunk in value.chunks]
        value.bm25 = BM25Okapi(tokenized_corpus)
        print("[INFO] BM25 index created")
        return value


    # ---------------- RRF FUSION ----------------
    def rrf_fusion(self, value,faiss_indices,bm25, k=60) -> Metadata:
        scores = {}
        for rank, idx in enumerate(faiss_indices):
            value.score[idx] = scores.get(idx, 0) + 1 / (k + rank)
        for rank, idx in enumerate(bm25):
            value.score[idx] = scores.get(idx, 0) + 1 / (k + rank)
        sorted_docs = sorted(value.score.items(), key=lambda x: x[1], reverse=True)
        value.sorted_doc = [doc[0] for doc in sorted_docs]
        return value