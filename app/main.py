from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(title="AI Product Idea Validator API", version="0.1.0")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://ai-product-validator.vercel.app",
     "https://ai-product-validator-r6264xxms-petera-majors-projects.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)