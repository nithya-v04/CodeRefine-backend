from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from orchestration import run_orchestration
from aggregator import aggregate

app = FastAPI()

class CodeInput(BaseModel):
    code_diff: str


@app.post("/analyze")
def analyze_code(input: CodeInput):
    try:
        review = run_orchestration(input.code_diff)
        final = aggregate(review)
        return final
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
