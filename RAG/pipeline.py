
from rag.RAG import C_rag
from utils.pdf_loader import C_load_pdf
from rag.index_creation import C_index
from rag.mcp import C_mcp
from rag.validation import C_validate


class C_pipeline:
    """def pipeline(self,value,value2):
        value.log.info('Inside pipeline')
        self.C_L_P=C_load_pdf()
        self.C_I=C_index(value)
        value.index_obj=self.C_I
        self.C_M=C_mcp()
        self.C_R=C_rag()
        self.C_V=C_validate()
        while True:
            self.C_L_P.load_pdf_context(value)
            self.C_L_P.build_semantic_text(value)
            self.C_L_P.split_into_chunks(value)
            self.C_I.create_faiss_index(value)
            self.C_I.create_bm25_index(value)
            self.C_M.create_MCP(value,value2)
            self.C_R.RAG(value,value2)
            self.C_V.rag_validate(value,value2)
            if len(value.missed)>0 or len(value.failed_validation)>0:
                value.log.info(f'validation failed Loop started for {value2.current_rag}')
                value.log.info(f'retry count ==>{value.retry_count}')
                value.log.info(f'Value Missed in LLM result {value.missed}')
                value.log.info(f'value Failed in LLM result is {value.failed_validation}')
                value.log.info(f'Semantic search used for above result is {value.L_semantic_search}')
                value.retry_count+=1
                if value.retry_count>3:
                    break
            elif value.pipeline_step<2:
                value.pipeline_step=2
                value.retry_count=0
                value2.current_rag=value.rag_result['Document category']
                value.log.info(f'Current Rag changed is {value2.current_rag}')
            else:
                break

            if value.retry_count > 3:
                break"""

    def data_processing(self,state):
        value=state.value
        self.C_L_P = C_load_pdf()
        self.C_L_P.load_pdf_context(value)
        self.C_L_P.build_semantic_text(value)
        self.C_L_P.split_into_chunks(value)

    def index_processing(self,state):
        value=state.value
        self.C_I = C_index(value)
        value.index_obj = self.C_I
        self.C_I.create_faiss_index(value)
        self.C_I.create_bm25_index(value)

    def model_context_protocal(self,state):
        value=state.value
        value2=state.value2
        self.C_M = C_mcp()
        self.C_M.create_MCP(value, value2)

    def call_LLM(self,state):
        value=state.value
        value2=state.value2
        self.C_R = C_rag()
        self.C_R.RAG(value, value2)

    def validate_result(self,state):
        value=state.value
        value2=state.value2
        self.C_V = C_validate()
        self.C_V.rag_validate(value, value2)

    def conditional_check(self,state):
        value=state.value
        value2=state.value2
        if len(value.missed) > 0 or len(value.failed_validation) > 0:
            value.log.info(f'validation failed Loop started for {value2.current_rag}')
            value.log.info(f'retry count ==>{value.retry_count}')
            value.log.info(f'Value Missed in LLM result {value.missed}')
            value.log.info(f'value Failed in LLM result is {value.failed_validation}')
            value.log.info(f'Semantic search used for above result is {value.L_semantic_search}')
            value.retry_count += 1
            if value.retry_count > 3:
                return 'END'
            return 'retry'
        elif value.pipeline_step < 2:
            value.pipeline_step = 2
            value.retry_count = 0
            value2.current_rag = value.rag_result['Document category']
            value.log.info(f'Current Rag changed is {value2.current_rag}')
            return 'retry'
        else:
            value.log.info(f'Program completed')
            return 'END'
