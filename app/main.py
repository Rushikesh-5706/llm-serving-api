from fastapi import FastAPI, Depends
from app.schemas import GenerateRequest, GenerateResponse
from app.auth import verify_api_key
from app.model import get_model
from app.config import MAX_WORKERS
from app.queue import request_semaphore
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI(title="LLM Serving API")

executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

@app.get("/health")
async def health():
    return {"status": "ok"}

def run_inference(prompt, max_new_tokens):
    model, tokenizer = get_model()
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest, api_key: str = Depends(verify_api_key)):
    async with request_semaphore:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            executor,
            run_inference,
            req.prompt,
            req.max_new_tokens
        )
        return {"generated_text": result}
