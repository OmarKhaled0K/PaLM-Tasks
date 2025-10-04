from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import retriever
from data_retriever.retriever import SimpleRetriever
from database.simple_data import SIMPLE_SNIPPETS
from prometheus_fastapi_instrumentator import Instrumentator
from middlewares.profiler import profile_http_middleware


instrumentator = Instrumentator()
simple_retriever = SimpleRetriever(
    snippets=SIMPLE_SNIPPETS
)

app = FastAPI(title="Retrieval Service",version="1.0.0",
    swagger_ui_parameters={"docExpansion": "none"},
)
app.middleware("http")(profile_http_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.simple_retriever = simple_retriever

app.include_router(retriever.router, prefix="/retriever", tags=["Retriever"])

@app.get("/")
def root():
    return {"message": "Retrieval API is running successfully."}

Instrumentator().instrument(app).expose(app, include_in_schema=True)