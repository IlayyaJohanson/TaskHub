from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.auth import router as auth_router

app = FastAPI(title="TaskHub API")


# Allow Vite dev server
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[
    #    "http://localhost:5173",
    #    "http://localhost:8000",
    #    "http://127.0.0.1:5173",
    #    "http://127.0.0.1:8000",
    # ],
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "TaskHub API is running"}


app.include_router(auth_router)
