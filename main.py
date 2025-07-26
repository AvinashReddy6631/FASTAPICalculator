from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Memory-based history
history = []

class Expression(BaseModel):
    expression: str

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/calculate")
def calculate(expr: Expression):
    try:
        result = eval(expr.expression, {"__builtins__": {}})
        history.append(f"{expr.expression} = {result}")
        return {"result": result}
    except Exception as e:
        return {"result": f"Error: {str(e)}"}

@app.get("/history")
def get_history():
    return {"history": history[-10:]}  # show last 10

@app.post("/clear")
def clear_history():
    history.clear()
    return {"message": "History cleared"}
