from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import io
import json
from contextlib import redirect_stdout

# Ensure the parent directory is in the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phase3_rfm_ab_testing import ab_test_funnel
from phase4_ai_action_engine import generate_recommendations

app = FastAPI(title="FinReach API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/ab-test")
@app.get("/ab-test")
def run_ab_test():
    f = io.StringIO()
    with redirect_stdout(f):
        ab_test_funnel(5000, 1000, 5000, 1150)
    output = f.getvalue()
    return {"status": "success", "output": output}

@app.get("/api/ai-action")
@app.get("/ai-action")
def run_ai_action():
    sample_data = [
        {"segment_name": "Champions", "avg_loan_size": 500, "repayment_rate": 0.98, "repeat_borrower_rate": 0.85},
        {"segment_name": "At Risk", "avg_loan_size": 150, "repayment_rate": 0.65, "repeat_borrower_rate": 0.10}
    ]
    f = io.StringIO()
    with redirect_stdout(f):
        generate_recommendations(sample_data)
    
    output = f.getvalue()
    try:
        json_output = json.loads(output)
        return {"status": "success", "data": json_output}
    except Exception as e:
        return {"status": "error", "output": output}
