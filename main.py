# ============================ IMPORT STATEMENTS ============================================
import os
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
from langchain_core.example_selectors import SemanticSimilarityExampleSelector

from config.few_shots import few_shots
from config.prompts import mysql_prompt, PROMPT_SUFFIX

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel


load_dotenv()
app = FastAPI()

model = ChatOpenAI(
    model=os.environ.get("MODEL"),
    openai_api_key=os.environ.get("OPENAI_API_KEY"),
    openai_api_base=os.environ.get("OPENAI_API_BASE"),
    # temperature=0.5
)

db_user = os.environ.get("db_user")
db_password = os.environ.get("db_password")
db_host = os.environ.get("db_host")
db_name = os.environ.get("db_name")
db_port = os.environ.get("db_port")

db = SQLDatabase.from_uri(
    f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorize = [" ".join(vector.values()) for vector in few_shots]


# vectorstore = Chroma.from_texts(texts=vectorize, embedding=embeddings, metadatas=few_shots)
vectorstore = Chroma.from_texts(
    texts=vectorize,
    embedding=embeddings,  # ← pass the wrapper, not raw embeddings
    metadatas=few_shots,
)


example_selector = SemanticSimilarityExampleSelector(vectorstore=vectorstore, k=2)


example_prompt = PromptTemplate(
    input_variables=[
        "Question",
        "SQLQuery",
        "SQLResult",
        "Answer",
    ],
    template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
)

few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix=mysql_prompt,
    suffix=PROMPT_SUFFIX,
    input_variables=["input", "table_info", "top_k"],
)

chain = SQLDatabaseChain.from_llm(model, db, verbose=False, prompt=few_shot_prompt)


# queryQuestion = "Which suppliers are performing significantly above normal in terms of total inventory value compared to other suppliers, but only among those suppliers whose products have not had any stockouts in the last 30 days, and whose average product price is above the overall average product price across the entire store? Also tell me by how much each of those suppliers exceeds the average supplier inventory value."
# result = chain.invoke({"query": queryQuestion})
# print(result)


# ============ ENDPOINTS ==========================

base_url = f"/v1/api"
class QueryRequest(BaseModel):
    query: str


@app.post(f"{base_url}/query")
async def get_result(payload: QueryRequest):
    print(payload)
    result = chain.invoke({"query": payload.query})
    return result
