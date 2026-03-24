import numpy as np
from rag.models import Metadata
from rag.index_creation import C_index
import logging
#from utils.index_manager import save_index, load_index



class C_retrieve():
    logger = logging.getLogger("RAG")
    def retrieve_context(self, question, value, k=10):
        if isinstance(question, list):
            question = " ".join(question)
        # -------- FAISS --------
        q_vec = value.embed_model.encode(question).astype("float32")
        if q_vec.ndim == 1:
            q_vec = np.array(q_vec).reshape(1, -1)

        D, I = value.index.search(q_vec, k)
        faiss_indices = I[0]
        # -------- BM25 --------
        tokenized_query = value.index_obj.tokenize(question)
        bm25_scores = value.bm25.get_scores(tokenized_query)
        bm25_indices = np.argsort(bm25_scores)[::-1][:k]
        # -------- Fusion --------
        final_indices = value.index_obj.rrf_fusion(value,faiss_indices, bm25_indices)
        final_indicex = final_indices.sorted_doc[:k]
        return [value.records[i].text for i in final_indicex]