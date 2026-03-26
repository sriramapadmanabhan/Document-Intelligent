import faiss
from rank_bm25 import BM25Okapi
from pydantic import BaseModel,Field,ConfigDict
from typing import Optional,List,Any,TypedDict,Union
from enum import Enum

class cons_type(str,Enum):
    type="type"
    min_length="min_length"
    max_length="max_length"
    location="type"
    alias="type"
    Integer="int"
    string="str"
    Numeric="Numeric"
    Alpha_numeric="Alpha-numeric"
    decimal="decimal"
    Date_time='Date and Time'

class semantic_metadata(BaseModel):
    section: Optional[str] = None
    page: Optional[int] = None
    table: Optional[int] = None
    ROW: Optional[Union[int,str]] = None
    heading: Optional[str] = None
    section_details: Optional[str] = None
    text:Optional[str]=None
    embedding:Optional[List[float]]=None

class Metadata(BaseModel):
    rows:Optional[List[semantic_metadata]]=None
    semantic_data:Optional[List[str]]=Field(default_factory=list)
    retry_count:Optional[int]=Field(default_factory=lambda :1)
    chunk_size:Optional[int]=Field(default_factory=lambda :300)
    chunk_overlap:Optional[int]=Field(default_factory=lambda :50)
    chunks:Optional[List[Any]]=Field(default_factory=list)
    embeddings:Optional[List[List[float]]] = None
    records:Optional[semantic_metadata]=Field(default_factory=list)
    vectors:Optional[List[List[float]]]=None
    index:Optional[faiss.IndexFlatL2]=None
    bm25:Optional[BM25Okapi]=None
    score:Optional[dict[Any,Any]]=Field(default_factory=dict)
    sorted_doc:Optional[list]=None
    task:Optional[str]=None
    field:Optional[list[Any]]=None
    rules:Optional[str]=None
    constraints:Optional[dict[str,dict[cons_type,Any]]]=None
    embed_model:Optional[Any]=None
    context:Optional[list[str]]=None
    index_obj:Optional[object]=None
    MCP:Optional[dict[str,Any]]=None
    rag_result:Optional[str]=None
    ntry:Optional[int]=Field(default_factory=lambda :0)
    missed:Optional[list[Any]]=Field(default_factory=list)
    missed_hist:Optional[list[Any]]=Field(default_factory=list)
    failed_validation:Optional[list[Any]]=Field(default_factory=list)
    failed_validation_hist: Optional[list[Any]] = Field(default_factory=list)
    pipeline_step:Optional[int]=Field(default_factory=lambda :0)
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Rag_status(BaseModel):
    current_rag:Optional[str]='summary'

class PipelineInput(BaseModel):
    M: Metadata
    R: Rag_status