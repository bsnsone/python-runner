from fastapi import FastAPI
from pydantic import BaseModel
from executor import run_python

app = FastAPI()

class RunReq(BaseModel):
    code: str
    packages: list[str] = []

@app.post("/run")
def run(req: RunReq):
    return {"output": run_python(req.code, req.packages)}
