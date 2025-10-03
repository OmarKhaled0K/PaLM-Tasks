from pydantic import BaseModel

class SimpleQueryRequest(BaseModel):
    query: str

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3
    metric: str = "cosine"
    weight: float | None = None
      