# ============================ IMPORT STATEMENTS ============================
import os
import asyncio

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from langchain_community.utilities import SQLDatabase
from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector

# from langchain_core.messages import HumanMessage
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_experimental.sql import SQLDatabaseChain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from config.few_shots import few_shots
from config.prompts import mysql_prompt, PROMPT_SUFFIX

# ============================ CONFIGURATION & INITIALIZATION ================

load_dotenv()
app = FastAPI()

# --- LLM ---
model = ChatOpenAI(
    model=os.environ.get("LLM"),
    openai_api_key=os.environ.get("OPENAI_API_KEY"),
    openai_api_base=os.environ.get("OPENAI_API_BASE"),
    # temperature=0.5
)

# --- Database ---
db_user = os.environ.get("db_user")
db_password = os.environ.get("db_password")
db_host = os.environ.get("db_host")
db_name = os.environ.get("db_name")
db_port = os.environ.get("db_port")

db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
db = SQLDatabase.from_uri(db_uri)

# ============================ VECTOR STORE & SQL CHAIN ======================

# --- Embeddings & vector store ---
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
vectorize = [" ".join(vector.values()) for vector in few_shots]

vectorstore = Chroma.from_texts(
    texts=vectorize,
    embedding=embeddings,
    metadatas=few_shots,
)

# --- Few-shot prompt & chain ---
example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=2,
)

example_prompt = PromptTemplate(
    input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
    template=(
        "\nQuestion: {Question}\nSQLQuery: {SQLQuery}\n"
        "SQLResult: {SQLResult}\nAnswer: {Answer}"
    ),
)

few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix=mysql_prompt,
    suffix=PROMPT_SUFFIX,
    input_variables=["input", "table_info", "top_k"],
)

chain = SQLDatabaseChain.from_llm(
    model,
    db,
    verbose=False,
    prompt=few_shot_prompt,
)

# ============================ API ENDPOINTS ================================

BASE_URL = "/v1/api"


class QueryRequest(BaseModel):
    query: str


@app.post(f"{BASE_URL}/query")
async def get_result(payload: QueryRequest):
    try:
        result = await asyncio.to_thread(chain.invoke, {"query": payload.query})
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}",
        )
