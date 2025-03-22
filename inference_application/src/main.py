from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.routes import classifier

app = FastAPI(
    title="NLP API",
    summary="Oasys Now Assignment",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(classifier.router)


@app.get("/", tags=["Landing"])
async def root():
    return {"message": "LANDING PAGE"}
