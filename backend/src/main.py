from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.supabase import supabase
from users import router as users_router
from bots import router as bots_router
from feedback import router as feedback_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def ping():
    return {"message": "pong"}


@app.get("/health")
def health_check():
    try:
        user = supabase.auth.get_user()
        return {"status": "ok", "supabase_connected": user}
    except Exception as error:
        return {"status": "error", "supabase_connected": error}
