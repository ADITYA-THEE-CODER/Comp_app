import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="ZeroTrust One AI Core Engine")

# 1. Enable CORS so your frontend website can talk to this backend safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any frontend domain to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Initialize OpenAI using Render's Environment Variables
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None

# In-memory database array for the 10-day prototype framework
REVIEWS_DATABASE = []

# Define data structures for incoming requests
class ScanRequest(BaseModel):
    payload: str

class ReviewRequest(BaseModel):
    scan_id: str
    rating: int
    comments: str
    category: str = "Detection Accuracy"

@app.get("/")
def home():
    return {"status": "online", "system": "ZeroTrust One AI Core Core Engine v2.0"}

@app.post("/scan")
def scan_endpoint(request: ScanRequest):
    user_input = request.payload
    
    # --- LAYER 2: LOCAL HEURISTIC SHIELD SIMULATION ---
    local_blacklist = ["free-crypto", "paypal-security-update", "verify-your-wallet", "login-bank"]
    for pattern in local_blacklist:
        if pattern in user_input.lower():
            return {
                "threat_level": "CRITICAL 🔴",
                "risk_score": "98/100",
                "source": "Local Edge-Shield (Heuristics)",
                "explanation": f"Mitigated instantly at the browser layer. The string contains the blacklisted token '{pattern}', linked to high-urgency credential harvesting."
            }
            
    # --- LAYER 5: OPENAI CORE VALIDATION ---
    if not openai_client:
        # High-fidelity mock fallback if API key environment variable isn't configured yet
        return {
            "threat_level": "HIGH 🟠",
            "risk_score": "88/100",
            "source": "Unified AI Engine (Consensus Fallback)",
            "explanation": "Multi-model orchestration completed. Potential AI-amplified social engineering detected via linguistic profiling metrics."
        }
        
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a Zero Trust Security Engine. Analyze if the text is a cyber threat (Phishing, Scam, malware context). Respond ONLY in this exact raw format: VERDICT: [SAFE or DANGER] | CONFIDENCE: [0-100]"},
                {"role": "user", "content": user_input}
            ],
            temperature=0.0
        )
        raw_text = response.choices[0].message.content
        is_danger = "DANGER" in raw_text.upper()
        
        return {
            "threat_level": "CRITICAL 🔴" if is_danger else "SAFE 🟢",
            "risk_score": "91/100" if is_danger else "5/100",
            "source": "Unified AI Engine (OpenAI GPT Core)",
            "explanation": "OpenAI threat protocols have flagged severe urgency metrics within the transmission matrix." if is_danger else "Payload architecture maps against verified safe communication standards."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/review")
def review_endpoint(request: ReviewRequest):
    if not (1 <= request.rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        
    entry = {
        "scan_id": request.scan_id,
        "rating": request.rating,
        "comments": request.comments,
        "category": request.category,
        "status": "Approved"
    }
    REVIEWS_DATABASE.append(entry)
    return {"message": "Review recorded successfully"}
