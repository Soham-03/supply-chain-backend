from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.risk import router as risk_router

app = FastAPI(title="Supply Chain Disruption Risk API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(risk_router)

@app.get("/")
def root():
    return {"message": "Supply Chain Risk API is running"}