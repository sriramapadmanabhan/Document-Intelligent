from rag.models import Metadata,Rag_status
from rag.pipeline import C_pipeline
from utils.logger import setup_logging
from rag.langgraph import run_pipeline


if __name__ == "__main__":
    log=setup_logging()
    log.info("Starting main Program")

    M=Metadata()
    M.log=log
    R=Rag_status()
    pipeline = C_pipeline()
    #result = pipeline.pipeline(M,R)
    result=run_pipeline(M,R)
