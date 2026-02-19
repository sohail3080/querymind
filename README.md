# Natural Language Q&A over MySQL (Retail Domain) with FastAPI & LangChain

Backend that lets users ask questions in plain English; questions are converted to SQL, run on a MySQL database, and answered with an LLM. Built for retail/product data with few-shot examples and semantic example selection.

---

## Postman Collection

You can test the API using the Postman collection below:

**Postman Collection:**  
[https://www.postman.com/myselfmdsohail-1533277/querymind/request/52316234-72d3d142-83e7-42c1-881b-73c53ce7d4ad/?action=share&creator=52316234&ctx=documentation](https://www.postman.com/myselfmdsohail-1533277/querymind/request/52316234-72d3d142-83e7-42c1-881b-73c53ce7d4ad/?action=share&creator=52316234&ctx=documentation)

---

## Running the Backend Locally

Start the FastAPI server with Uvicorn:

```bash
uvicorn main:app --reload
```

---

## Routes

| Route            | Method | Use                                                                 |
|------------------|--------|----------------------------------------------------------------------|
| `/v1/api/query`  | POST   | Send a natural language question; backend generates SQL, runs it on MySQL, and returns an LLM answer. |

---

## Payloads

### POST `/v1/api/query`

**Body**

```json
{
  "query": "What electronics items cost less than 50 dollars?"
}
```

The backend uses few-shot examples (selected by semantic similarity from a Chroma vector store), the MySQL schema, and an OpenAI-compatible LLM to produce SQL, execute it, and format the answer.

---

## Environment Variables

| Variable           | Description |
|--------------------|-------------|
| `OPENAI_API_KEY`   | API key for the LLM (OpenAI or compatible endpoint). |
| `OPENAI_API_BASE`  | Base URL for the API (e.g. `https://api.openai.com/v1` or your custom endpoint). |
| `LLM`              | Model name/id (e.g. `gpt-4`, `gpt-3.5-turbo`). |
| `EMBEDDING_MODEL`  | HuggingFace model for few-shot example embeddings (default used: `sentence-transformers/all-MiniLM-L6-v2`). |
| `db_user`          | MySQL user (readonly recommended). |
| `db_password`      | MySQL password. |
| `db_host`          | MySQL host. |
| `db_name`          | Database name. |
| `db_port`          | MySQL port (e.g. `3306`). |

Copy `.env.example` to `.env` and fill in your values.

---

## Chain-of-Thought & Few Shots (brief)

- **Chain-of-thought (CoT):** The system prompt in `config/prompts.py` asks the LLM to reason step-by-step (understand the question → identify tables/columns → construct filters → ordering/limits) and output that reasoning before writing the SQL. This improves accuracy and debuggability.
- **Few shots:** Example question–SQL–answer pairs live in `config/few_shots.py`. The 2 most semantically similar examples to the user’s question are retrieved from Chroma and injected into the prompt so the model can mimic style and patterns (e.g. price ranges, categories, suppliers).

---

## Architecture Notes

1. **Text-to-SQL with few-shot learning** — Natural language → SQL via LangChain `SQLDatabaseChain` and a MySQL-focused system prompt.
2. **Semantic example selection** — Few-shot examples are stored in Chroma; the 2 most similar examples to the user question are selected (HuggingFace embeddings).
3. **Retail-oriented prompts** — Prompts and examples in `config/prompts.py` and `config/few_shots.py` target product name search, categories, price ranges, stock, and suppliers.
4. **Stateless FastAPI backend** — Single query endpoint; no auth in the current code (add middleware if needed).

---

## Limitations & Considerations

- **Database access** — Use a **readonly** MySQL user for safety; the app runs generated SELECT queries.
- **LLM dependency** — Requires an OpenAI-compatible API (OpenAI or custom base URL). No built-in API key auth in the app; secure the endpoint (e.g. reverse proxy or FastAPI middleware) if exposed.
- **Few-shot scope** — Example set is fixed in code; best results when questions align with the retail schema and example types (prices, categories, stock, suppliers, etc.).
- **No streaming** — Response is returned in one shot after SQL execution and LLM reply.

---

## Sources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Virtual environments \| FastAPI](https://fastapi.tiangolo.com/virtual-environments/)
- [Youtube video](https://youtu.be/d4yCWBGFCEs?si=y-t0Mjn15qlhqitU)
- [Permission for a user in mysql workbench](https://stackoverflow.com/questions/11202434/read-only-privilege-for-a-user-in-mysql-work-bench)
- [Agents](https://docs.langchain.com/oss/python/langchain/agents)
- [LangChain SQL Chain](https://python.langchain.com/docs/integrations/toolkits/sql_database)
- [ChatGoogleGenerativeAI integration](https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai)
- [Chroma Documentation](https://docs.trychroma.com/)
- [HuggingFace Sentence Transformers](https://www.sbert.net/)
- [SQLDatabase \| LangChain Community](https://python.langchain.com/docs/integrations/tools/sql_database)
- [Few-shot prompting](https://www.promptingguide.ai/techniques/fewshot)
- [Chain-of-thought prompting](https://www.promptingguide.ai/techniques/cot)

---

## Additional Note

This is a learning project to combine **natural language Q&A**, **Text-to-SQL**, **FastAPI**, **LangChain**, **Chroma** (for few-shot retrieval), and **MySQL** in a retail context. It is intended for experimentation and understanding the stack, not as a production-ready service.

---

## Feedback

If you find a bug, have a suggestion, or want to report an issue, please open an issue or reach out; feedback is welcome.

**LinkedIn:** [example.link](www.linkedin.com/in/md-sohail-230141205) *(replace with your LinkedIn profile URL)*
