import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_recommendations(rfm_data):
    """
    rfm_data: list of dicts with segment metrics
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    prompt = f"""
    You are an expert product growth manager and data scientist for a digital micro-lending app called FinReach.
    I will provide you with RFM (Recency, Frequency, Monetary) segmentation data for our user base.
    
    For each segment, I need you to output exactly 3 concrete, business-focused growth actions (next-best-actions).
    
    RULES:
    1. Your output MUST be strictly valid JSON in the following format:
    {{
        "segments": [
            {{
                "segment_name": "String",
                "actions": ["Action 1", "Action 2", "Action 3"]
            }}
        ]
    }}
    2. You must specifically cite the provided metrics (e.g., "Given the low repayment rate of X%...").
    3. NO generic fluff. Actions must be specific to micro-lending (e.g., rate discounts, reminder SMS, grace periods, upsell on next loan).
    
    DATA:
    {json.dumps(rfm_data, indent=2)}
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        try:
            content = result['candidates'][0]['content']['parts'][0]['text']
            # strip markdown formatting if any
            if content.startswith('```json'):
                content = content[7:-3]
            elif content.startswith('```'):
                content = content[3:-3]
            print(json.dumps(json.loads(content), indent=2))
        except KeyError as e:
            print("Failed to parse Gemini response:", result)
    else:
        print(f"Error calling Gemini API: {response.text}")

if __name__ == "__main__":
    sample_data = [
        {"segment_name": "Champions", "avg_loan_size": 500, "repayment_rate": 0.98, "repeat_borrower_rate": 0.85},
        {"segment_name": "At Risk", "avg_loan_size": 150, "repayment_rate": 0.65, "repeat_borrower_rate": 0.10}
    ]
    generate_recommendations(sample_data)
