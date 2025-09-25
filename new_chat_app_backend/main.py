from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_user, routes_auth, routes_message, routes_ws
from app.db.base import Base
from app.db.session import init_models


app = FastAPI(title="Chat App")

# CORS (so frontend can access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes_user.router, prefix="/users", tags=["users"])
app.include_router(routes_auth.router, prefix="/auth", tags=["auth"])
app.include_router(routes_message.router, prefix="/messages", tags=["messages"])
app.include_router(routes_ws.router, prefix="/ws", tags=["ws"])

@app.on_event("startup")
async def on_startup():
    await init_models() 

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Chat App API is running!"}


