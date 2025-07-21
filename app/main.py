from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import duckdb
import os

from app.bootstrap import fetch_duckdb_from_s3

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
    # TEMP: Hardcoded SQL query for demo
    sql = """
        SELECT state, species, unit, total_harvest, percent_success
        FROM harvest_production
        WHERE species = 'elk' AND year = 2023
        LIMIT 5;
    """
    print("🔍 DB_PATH:", DB_PATH)
    print("🧠 Tables in database:")
    try:
        conn = duckdb.connect(DB_PATH)
        print(conn.execute("SHOW TABLES").fetchall())
    except Exception as e:
        print("❌ Failed to open DuckDB or list tables:", e)
        raise

    result = conn.execute(sql).fetchall()
    conn.close()

    return templates.TemplateResponse(
        "partials/result.html",
        {"request": request, "question": question, "results": result},
    )
