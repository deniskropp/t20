import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from t20_api.database import engine, Base
from t20_api.routers import workflow, prompts

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB: Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Initialize System (Workflow)
    await workflow.initialize_system(orchestrator_name="Meta-AI")
    
    yield
    
    # Shutdown System
    await workflow.shutdown_system()

app = FastAPI(
    title="Multi-Agent Workflow API (G2)",
    version="2.1.0",
    description="API for orchestrating multi-agent workflows and managing prompts.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workflow.router)
app.include_router(prompts.router)

def main():
    print("Starting T20 API server on http://localhost:8000")
    uvicorn.run("t20_api.main:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    main()
