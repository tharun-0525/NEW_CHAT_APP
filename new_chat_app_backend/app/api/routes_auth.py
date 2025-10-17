from fastapi import APIRouter, Depends, Form, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.user_services import createUser, getUserByUsername, getUsers, login_user
from app.core.security import verify_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schema.user import UserCreate, UserLogin


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/login")
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    try:
        token = await login_user(form.username, form.password, db)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"access_token": token, "token_type": "bearer"}

    except HTTPException: 
        raise

    except ValueError as e: 
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong on our side")

@router.post("/register")
async def register_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await getUserByUsername(db, data.username)
    if existing_user:
        return {"error": "Username already exists"}
    try:
        user = await createUser(db, data.name, data.email, data.username, data.password)
        return {"id": user.id, "username": user.username, "email": user.email}
    except Exception:
        if(status.HTTP_422_UNPROCESSABLE_ENTITY):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid data provided")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_token(token)
        return {"user_id": payload.get("user_id")}
                
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")