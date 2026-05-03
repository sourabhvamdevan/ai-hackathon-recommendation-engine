
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.rag_engine import BISRagEngine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = BISRagEngine()

class Inquiry(BaseModel):
    product_description: str

@app.post("/api/discover")
async def discover(inquiry: Inquiry):
    response = engine.get_recommendations(inquiry.product_description)
    return {"success": True, "data": response["text"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)