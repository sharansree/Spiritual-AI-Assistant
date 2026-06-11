from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, questions

app = FastAPI(
    title="Sathya API",
    description="Buddhist wisdom grounded in the Pali Canon",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(questions.router)

@app.get("/health")
def health():
    return {"status": "ok", "message": "Sathya API is running"}