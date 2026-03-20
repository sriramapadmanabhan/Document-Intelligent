from langchain_text_splitters import RecursiveCharacterTextSplitter
import subprocess
import json

from rag.retriever import Retriever
from utils.pdf_loader import load_pdf


class RAGPipeline:

    def __init__(self):
        self.retriever = Retriever()

    def build_text(self, value):
        for block in value.rows:
            text = f"Page:{block.page}, Heading:{block.heading}, Details:{' '.join(block.section_details or [])}"
            value.semantic_data.append(text)
        return value

    def chunk(self, value):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=value.chunk_size,
            chunk_overlap=value.chunk_overlap
        )

        for t in value.semantic_data:
            value.chunks.extend(splitter.split_text(t))

        return value

    def instructions(self, value):

        if value.current_rag == "summary":
            value.task = "summarize document"
            value.field = ["summary"]

        elif value.current_rag == "Railways":
            value.task = "extract railway fields"
            value.field = ["PNR", "seat number"]

        context = self.retriever.retrieve(value.field, value)
        value.context = "\n".join(context)

        return value

    def call_llm(self, value):

        prompt = f"""
You are an extractor.

{json.dumps({
    "task": value.task,
    "fields": value.field,
    "context": value.context
}, indent=2)}
"""

        result = subprocess.run(
            ["ollama", "run", "mixtral", prompt],
            capture_output=True,
            text=True
        )

        value.rag_result = result.stdout.strip()

        return value

    def run(self, value):

        load_pdf(value)
        self.build_text(value)
        self.chunk(value)

        self.retriever.create_faiss(value)
        self.retriever.create_bm25(value)

        if not value.current_rag:
            value.current_rag = "summary"

        self.instructions(value)
        self.call_llm(value)

        return value