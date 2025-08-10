# app.py
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import asyncio
from agent_service import run_agent

app = FastAPI(title="Agente MCP API")

class PromptRequest(BaseModel):
    prompt: str

@app.post("/run")
async def run_prompt(req: PromptRequest):
    output = await run_agent(req.prompt)
    return {"result": output}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
