from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import quotes

api_root_ver = "/api/v1"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quotes.router, prefix=f"{api_root_ver}", tags=["Quotes"])
