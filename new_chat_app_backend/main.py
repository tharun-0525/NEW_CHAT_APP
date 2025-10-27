from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_user, routes_auth, routes_message, routes_ws
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.db.session import init_models
from app.schema.response import ResponseModel


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

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseModel(
            status="failed",
            message=exc.detail
        ).model_dump(),
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("Validation error:", exc)
    err=exc.errors()
    print("First error detail:", err)
    return JSONResponse(
        status_code=422,
        content=ResponseModel(
            status="failed",
            message="Validation error",
            data=err
        ).model_dump(),
    )

