from typing import Annotated
from sqlmodel import text, Session
from src.models import db
from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def show_sql_form(request: Request):
    """Muestra el formulario para ingresar consultas SQL"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
def execute_sql_query(
    request: Request,
    sql_query: Annotated[str, Form()],
    session: Annotated[Session, Depends(db.get_session)]
):
    """Ejecuta la consulta SQL y muestra los resultados"""
    
    # Limpiar la consulta
    query = sql_query.strip()
    
    # Validar que no esté vacía
    if not query:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "query": query,
            "error": "Por favor ingresa una consulta SQL."
        })
    
    try:
        # Ejecutar la consulta
        result = session.execute(text(query))
        rows = result.fetchall()
        
        # Obtener nombres de columnas
        columns = list(result.keys()) if rows else []
        
        # Convertir filas a diccionarios
        results = []
        for row in rows:
            row_dict = {}
            for i, column in enumerate(columns):
                row_dict[column] = row[i] if i < len(row) else None
            results.append(row_dict)
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "query": query,
            "results": results,
            "columns": columns
        })
        
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "query": query,
            "error": str(e)
        })


