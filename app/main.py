from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.api import projects, optimize, frontier

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Innovation Portfolio Optimizer", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(optimize.router, prefix="/api/optimize", tags=["optimize"])
app.include_router(frontier.router, prefix="/api/frontier", tags=["frontier"])

@app.get("/health")
def health():
    return {"status": "ok"}
