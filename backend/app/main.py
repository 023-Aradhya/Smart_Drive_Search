from fastapi import FastAPI
from pydantic import BaseModel
from agent_setup import agent

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    response = agent.invoke({
        "input": req.message
    })
    output = response["output"]
    return {
        "response": str(output)
    }