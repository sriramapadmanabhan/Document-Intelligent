from langgraph.graph import StateGraph, END
from rag.pipeline import C_pipeline
from pydantic import BaseModel
from typing import Any


class PipelineState(BaseModel):
    value: Any
    value2: Any

C_P=C_pipeline()
builder = StateGraph(PipelineState)
builder.add_node("load_pdf", C_P.data_processing)
builder.add_node("index", C_P.index_processing)
builder.add_node("mcp", C_P.model_context_protocal)
builder.add_node("rag", C_P.call_LLM)
builder.add_node("validate", C_P.validate_result)

builder.add_edge("load_pdf","index")
builder.add_edge("index","mcp")
builder.add_edge("mcp","rag")
builder.add_edge("rag","validate")
builder.add_conditional_edges("validate",C_P.conditional_check,{"retry": "load_pdf","end": END})