from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import duckdb
import os

from app.bootstrap import fetch_duckdb_from_s3
from app.nl2sql import generate_sql_from_question
from app.safe_sql import is_safe_sql, is_safe_question

DB_PATH = fetch_duckdb_from_s3()

app = FastAPI()

# Mount static files and template engine
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/ask", response_class=HTMLResponse)
def ask_question(request: Request, question: str = Form(...)):
    if not is_safe_question(question):
        return templates.TemplateResponse(
            "partials/result.html",
            {
                "request": request,
                "question": question,
                "sql": "",
                "columns": [],
                "rows": [],
                "error": "Unsafe question detected. Please rephrase your question.",
            },
        )

    try:
        sql = generate_sql_from_question(question)
        if not is_safe_sql(sql):
            return templates.TemplateResponse(
                "partials/result.html",
                {
                    "request": request,
                    "question": question,
                    "sql": sql,
                    "columns": [],
                    "rows": [],
                    "error": "Unsafe SQL detected. Please rephrase your question.",
                },
            )

        with duckdb.connect(DB_PATH) as conn:
            try:
                result = conn.execute(sql).fetchall()
                columns = [desc[0] for desc in conn.description]
            except Exception as e:
                print(f"SQL execution error: {e}")

        return templates.TemplateResponse(
            "partials/result.html",
            {
                "request": request,
                "question": question,
                "sql": sql,
                "columns": columns,
                "rows": result,
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            "partials/result.html",
            {
                "request": request,
                "question": question,
                "error": str(e),
                "columns": [],
                "rows": [],
            },
        )
