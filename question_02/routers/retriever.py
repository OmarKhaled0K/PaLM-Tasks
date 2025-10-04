from fastapi import APIRouter,Request
from schemas.request import QueryRequest, SimpleQueryRequest
from database.simple_data import DENYLIST
router = APIRouter()
def is_safe_query(query: str) -> bool:
    query_lower = query.lower()
    return not any(bad in query_lower for bad in DENYLIST)

@router.post("/answer")
async def get_answer(request: Request, body: SimpleQueryRequest):
    if not is_safe_query(body.query):
        return {"error": "Query contains forbidden content."}
    retriever = request.app.state.simple_retriever 
    answer,top_chunks = retriever.retrieve(body.query, top_k=3)  
    return {
        "query": body.query,
        "answer":answer,
        "top_chunks": top_chunks,
    }

@router.post("/bm25")
async def bm25_retriever(request: Request, body: QueryRequest):
    if not is_safe_query(body.query):
        return {"error": "Query contains forbidden content."}
    retriever = request.app.state.simple_retriever 
    answer,top_chunks = retriever.retrieve(body.query,retriever_type="bm25", top_k=body.top_k)  
    return {
        "query": body.query,
        "answer":answer,
        "retriever": "bm25",
        "top_k": body.top_k,
        "top_chunks": top_chunks,
    }

@router.post("/vector")
async def vector_retriever(request: Request, body: QueryRequest):
    if not is_safe_query(body.query):
        return {"error": "Query contains forbidden content."}
    retriever = request.app.state.simple_retriever 
    answer,top_chunks = retriever.retrieve(body.query,retriever_type="faiss", top_k=body.top_k,metric=body.metric,) 
    return {
        "query": body.query,
        "answer":answer,
        "retriever": "vector",
        "top_k": body.top_k,
        "metric":body.metric,
        "top_chunks": top_chunks,
    }

@router.post("/hybrid")
async def hybrid_retriever(request: Request, body: QueryRequest):
    if not is_safe_query(body.query):
        return {"error": "Query contains forbidden content."}
    retriever = request.app.state.simple_retriever 
    answer,top_chunks = retriever.retrieve(body.query,retriever_type="hybrid", top_k=body.top_k,metric=body.metric, weights=body.weight) 
    return {
        "query": body.query,
        "answer":answer,
        "retriever": "hybrid",
        "top_k": body.top_k,
        "metric":body.metric,
        "weight": body.weight or 0.5,
        "top_chunks": top_chunks,
    }
