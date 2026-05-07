from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.api.routes import router
from app import db
import os

load_dotenv()

app = FastAPI(
    title="First Back-End API",
    version="0.1.0",
    description="Starter FastAPI project",
)

# simple CORS for local frontend development
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
def on_startup():
    db.init_db()


@app.on_event("shutdown")
def on_shutdown():
    db.close_pool()


@app.get("/", tags=["Root"])
def read_root() -> dict[str, str]:
    return {"message": "Welcome to the First Back-End API"}
