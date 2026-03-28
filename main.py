from rag.models import Metadata,Rag_status
from rag.pipeline import C_pipeline
from utils.logger import setup_logging


if __name__ == "__main__":
    log=setup_logging()
    log.info("Starting Pipeline")

    M=Metadata()
    M.log=log
    R=Rag_status()
    pipeline = C_pipeline()
    result = pipeline.pipeline(M,R)

    #result = C_validate()

    #print("\n=== RESULT ===\n")
    #print(result.rag_result)

    #print("\n=== VALIDATION ===\n")
    #print(result.rag_status)