from pydantic import BaseModel, Field
from typing import Optional, List, Any, Union
from enum import Enum


class cons_type(str, Enum):
    type = "type"
    min_length = "min_length"
    max_length = "max_length"
    location = "location"
    alias = "alias"


class semantic_metadata(BaseModel):
    section: Optional[str] = None
    page: Optional[int] = None
    table: Optional[int] = None
    ROW: Optional[Union[int, str]] = None
    heading: Optional[str] = None
    section_details: Optional[List[str]] = None
    text: Optional[str] = None
    embedding: Optional[List[float]] = None


class Metadata(BaseModel):
    rows: Optional[List[semantic_metadata]] = None
    semantic_data: List[str] = Field(default_factory=list)
    retry_count: int = 0
    chunk_size: int = 300
    chunk_overlap: int = 50
    chunks: List[str] = Field(default_factory=list)
    embeddings: Optional[List[List[float]]] = None
    records: List[semantic_metadata] = Field(default_factory=list)
    vectors: Optional[Any] = None
    index: Optional[Any] = None
    bm25: Optional[Any] = None
    score: dict = Field(default_factory=dict)
    sorted_doc: List[int] = Field(default_factory=list)
    task: Optional[str] = None
    field: Optional[List[Any]] = None
    rules: Optional[str] = None
    constraints: Optional[dict] = None
    context: Optional[str] = None
    MCP: Optional[dict] = None
    rag_result: Optional[str] = None
    ntry: int = 0
    rag_status: dict = Field(default_factory=dict)
    current_rag: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True