from langchain_text_splitters import RecursiveCharacterTextSplitter
import subprocess
import json
from rag.retriever import C_retrieve
from utils.pdf_loader import C_load_pdf
from rag.models import Rag_status,Metadata
from utils.pdf_loader import C_load_pdf
from rag.index_creation import C_index
from rag.mcp import C_mcp
from rag.validation import C_validate
import logging

class C_pipeline:
    logger = logging.getLogger("RAG")
    def pipeline(self,value,value2):
        self.C_L_P=C_load_pdf()
        self.C_I=C_index(value)
        value.index_obj=self.C_I
        self.C_M=C_mcp()
        self.C_V=C_validate()
        while True:
            self.C_L_P.load_pdf_context(value)
            self.C_L_P.build_semantic_text(value)
            self.C_L_P.split_into_chunks(value)
            self.C_I.create_faiss_index(value)
            self.C_I.create_bm25_index(value)
            self.C_M.create_MCP(value,value2)
            self.C_V.rag_validate(value,value2)
            for i in range(5):
                if len(value.missed)>0 or len(value.failed_validation)>0:
                    print('haiiii')
                    print('retry count ==>',value.retry_count)
                    print(value.missed,'->>',value.failed_validation)
                    value.missed_hist.append( value.missed)
                    value.missed=[]
                    value.missed_hist.append(value.failed_validation)
                    value.failed_validation=[]
                    value.retry_count+=1
                    if value.retry_count>3:
                        break
                elif value.pipeline_step<2:
                    print('baiii')
                    value.pipeline_step=2
                    value.retry_count=1
                    value2.current_rag=value.rag_result['Document category']
                else:
                    break

            if value.retry_count > 3:
                break

