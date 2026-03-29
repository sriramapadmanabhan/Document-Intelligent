import numpy as np
import logging


class C_retrieve():
    logger = logging.getLogger("RAG")
    def retrieve_context(self, question, value, k=20):
        if isinstance(question, list):
            question = " ".join(question)

        q_vec = value.embed_model.encode(question).astype("float32")
        if q_vec.ndim == 1:
            q_vec = np.array(q_vec).reshape(1, -1)

        D, I = value.index.search(q_vec, k)
        a=[]
        for i in I[0]:
            print(value.records[i].text)


        faiss_indices = I[0]
        tokenized_query = value.index_obj.tokenize(question)
        bm25_scores = value.bm25.get_scores(tokenized_query)
        bm25_indices = np.argsort(bm25_scores)[::-1][:k]

        final_indices = value.index_obj.rrf_fusion(value,faiss_indices, bm25_indices)
        final_indicex = final_indices.sorted_doc[:k]
        value.L_semantic_search=[value.records[i].text for i in final_indicex]
        return [value.records[i].text for i in final_indicex]