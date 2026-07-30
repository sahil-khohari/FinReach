from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sys
import os

# Ensure the parent directory is in the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phase3_rfm_ab_testing import ab_test_funnel
import io
from contextlib import redirect_stdout

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "FinReach Analytics API is deployed successfully."}

@app.get("/ab-test")
def run_ab_test():
    f = io.StringIO()
    with redirect_stdout(f):
        ab_test_funnel(5000, 1000, 5000, 1150)
    output = f.getvalue()
    return {"status": "success", "output": output}
