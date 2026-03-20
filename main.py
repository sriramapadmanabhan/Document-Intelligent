from rag.models import Metadata
from rag.pipeline import RAGPipeline
from rag.validator import validate


if __name__ == "__main__":

    meta = Metadata()
    pipeline = RAGPipeline()

    result = pipeline.run(meta)

    result = validate(result)

    print("\n=== RESULT ===\n")
    print(result.rag_result)

    print("\n=== VALIDATION ===\n")
    print(result.rag_status)