from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from executor import run_python

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class RunReq(BaseModel):
    code: str
    packages: list[str] = []

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/run")
def run(req: RunReq):
    output = run_python(req.code, req.packages)
    return {"output": output}
