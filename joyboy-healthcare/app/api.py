# policy_api.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()
# Allow requests from Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] for testing only (not production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
POLICY_FILE = "policy.txt"

class PolicyUpdate(BaseModel):
    new_policy: str
    role: str

@app.get("/policy")
async def get_policy():
    with open(POLICY_FILE, "r") as f:
        return {"policy": f.read()}

@app.post("/update_policy")
async def update_policy(update: PolicyUpdate):
    if update.role != "admin":
        return {"status": "error", "message": "Unauthorized"}
    
    with open(POLICY_FILE, "w") as f:
        f.write(update.new_policy)
    
    return {"status": "success", "message": "Policy updated"}
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)