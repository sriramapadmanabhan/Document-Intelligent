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


class C_pipeline:
    def pipeline(self,value,value2):
        self.C_L_P=C_load_pdf()
        self.C_I=C_index(value)
        value.index_obj=self.C_I
        self.C_M=C_mcp()
        self.C_V=C_validate()
        self.C_L_P.load_pdf_context(value)
        self.C_L_P.build_semantic_text(value)
        self.C_L_P.split_into_chunks(value)
        self.C_I.create_faiss_index(value)
        self.C_I.create_bm25_index(value)
        if value2.current_rag is None:
            value2.current_rag ='summary'
        self.C_M.create_MCP(value,value2)
        self.C_V.rag_validate(value)