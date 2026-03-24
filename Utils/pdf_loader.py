from utils import Read_pdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.models import Metadata, semantic_metadata


class C_load_pdf():
    def load_pdf_context(self,value: Metadata) -> Metadata:
        if value.rows is None:
            obj = Read_pdf.R_PDF()
            obj.get_page_details()
            rows = obj.convert_to_data()
            structured_blocks = obj.semantic(rows)
            value.rows = [semantic_metadata(**i) for i in structured_blocks]
            return value


    def build_semantic_text(self,value: Metadata) -> Metadata:
        for block in value.rows:
            heading = block.heading or ''
            details = " ".join(block.section_details or [])
            page_no = block.page or ''
            row_number = block.ROW or ''
            table_no = block.table or ''
            text = f""" Page related details page-no : {page_no}, Table-no : {table_no}, Row-no : {row_number},Section-Heading related details: {heading},Section-Details: {details} """.strip()
            value.semantic_data.append(text)
        return value


    def split_into_chunks(self, value: Metadata) -> Metadata:
        if value.retry_count == 1:
            value.chunk_size = 500
            value.chunk_overlap = 50
        if value.retry_count == 2:
            value.chunk_size = 200
            value.chunk_overlap = 50
        elif value.retry_count == 3:
            value.chunk_size = 400
            value.chunk_overlap = 50
        splitter = RecursiveCharacterTextSplitter(chunk_size=value.chunk_size, chunk_overlap=value.chunk_overlap,separators=["\n\n", "\n", ".", " ", ""])
        for t in value.semantic_data:
            value.chunks.extend(splitter.split_text(t))
        return value