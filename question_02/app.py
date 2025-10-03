from fastapi import FastAPI
from routers import retriever
from data_retriever.retriever import SimpleRetriever
from database.simple_data import SIMPLE_SNIPPETS
simple_retriever = SimpleRetriever(
    snippets=SIMPLE_SNIPPETS
)

app = FastAPI(title="Retrieval Service")
app.state.simple_retriever = simple_retriever

app.include_router(retriever.router, prefix="/retriever", tags=["Retriever"])

@app.get("/")
def root():
    return {"message": "Retrieval API is running successfully."}
