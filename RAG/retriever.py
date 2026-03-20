import numpy as np
import faiss
import re
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi


class Retriever:

    def __init__(self):
        self.embed_model = SentenceTransformer("all-MiniLM-L6-v2")

    def tokenize(self, text):
        return re.findall(r"\w+", text.lower())

    def create_faiss(self, value):
        value.embeddings = self.embed_model.encode(value.chunks)

        for text, emb in zip(value.chunks, value.embeddings):
            value.records.append({"text": text, "embedding": emb.tolist()})

        value.vectors = np.array([r["embedding"] for r in value.records]).astype("float32")

        index = faiss.IndexFlatL2(value.vectors.shape[1])
        index.add(value.vectors)

        value.index = index
        return value

    def create_bm25(self, value):
        tokenized = [self.tokenize(c) for c in value.chunks]
        value.bm25 = BM25Okapi(tokenized)
        return value

    def rrf(self, faiss_idx, bm25_idx, k=60):
        scores = {}

        for rank, idx in enumerate(faiss_idx):
            scores[idx] = scores.get(idx, 0) + 1 / (k + rank)

        for rank, idx in enumerate(bm25_idx):
            scores[idx] = scores.get(idx, 0) + 1 / (k + rank)

        return sorted(scores, key=scores.get, reverse=True)

    def retrieve(self, query, value, k=10):

        if isinstance(query, list):
            query = " ".join(query)

        q_vec = self.embed_model.encode([query]).astype("float32")

        _, I = value.index.search(q_vec, k)
        faiss_idx = I[0]

        bm25_scores = value.bm25.get_scores(self.tokenize(query))
        bm25_idx = np.argsort(bm25_scores)[::-1][:k]

        final = self.rrf(faiss_idx, bm25_idx)[:k]

        return [value.records[i]["text"] for i in final]