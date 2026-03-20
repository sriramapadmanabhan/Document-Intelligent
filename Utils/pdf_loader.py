import Read_pdf
from rag.models import semantic_metadata, Metadata


def load_pdf(value: Metadata) -> Metadata:
    if value.rows is None:
        obj = Read_pdf.R_PDF()
        obj.get_page_details()
        rows = obj.convert_to_data()
        structured_blocks = obj.semantic(rows)
        value.rows = [semantic_metadata(**i) for i in structured_blocks]
    return value