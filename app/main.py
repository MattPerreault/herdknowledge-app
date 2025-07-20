from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import duckdb
import os

app = FastAPI()

# Mount static files and template engine
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Replace with your actual DuckDB path
DB_PATH = os.getenv("DUCKDB_PATH", "data/database/herd_data.duckdb")

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
    conn = duckdb.connect(DB_PATH)
    result = conn.execute(sql).fetchall()
    conn.close()

    return templates.TemplateResponse("partials/result.html", {
        "request": request,
        "question": question,
        "results": result
    })
