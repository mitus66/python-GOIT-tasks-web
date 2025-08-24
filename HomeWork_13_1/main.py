# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from jose import jwt, JWTError

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis
import asyncio

import cloudinary
import cloudinary.uploader
from fastapi.middleware.cors import CORSMiddleware

import email as mail_service
from database import engine, get_db
from schemas import Contact as ContactSchema, ContactCreate, ContactUpdate, User as UserSchema, UserCreate, Token
import crud, users, auth
from models import User, Contact
from config import settings

# ---
## Налаштування Redis для FastAPILimiter

# Використання lifespan для ініціалізації ресурсів
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Async context manager for managing application lifespan events.
    Initializes Redis connection for FastAPILimiter on startup.
    """
    # Логіка, що виконується під час запуску (startup)
    redis_conn = redis.Redis(host='redis', port=6379, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_conn)
    print("FastAPILimiter initialized with Redis.")
    yield
    # Логіка, що виконується під час зупинки (shutdown)
    # Тут можна додати очищення ресурсів, якщо потрібно

# ---
## Ініціалізація FastAPI

app = FastAPI(
    title="Contacts API",
    description="REST API для зберігання та управління контактами з FastAPI та SQLAlchemy.",
    version="1.0.0",
    lifespan=lifespan # Використання lifespan замість app.on_event("startup")
)

# Створення таблиць у базі даних.
models.Base.metadata.create_all(bind=engine)

# ---
## Конфігурація сервісів

# Налаштування Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

# Налаштування CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://your-frontend-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---
## Ендпоїнти користувачів

@app.patch("/users/avatar", response_model=UserSchema)
async def update_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update the user's avatar by uploading a file to Cloudinary.
    """
    try:
        result = cloudinary.uploader.upload(file.file, folder="avatars")
        avatar_url = result.get("secure_url")
        current_user.avatar = avatar_url
        db.commit()
        db.refresh(current_user)
        return current_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/signup", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Register a new user and send a verification email.
    """
    db_user = users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    new_user = users.create_user(db=db, user=user)

    background_tasks.add_task(mail_service.send_email_verification, new_user.email, new_user.email, settings.FRONTEND_URL)

    return new_user


@app.get("/verify-email/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    """
    Verify user's email using a JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise credentials_exception
        if user.is_verified:
            return {"message": "Email already verified"}

        user.is_verified = True
        db.commit()
        return {"message": "Email successfully verified"}
    except JWTError:
        raise credentials_exception


@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Log in a user and get access and refresh tokens.
    """
    user = users.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = auth.create_refresh_token(
        data={"sub": user.email}, expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# ---
## Ендпоїнти контактів

@app.post("/contacts/", response_model=ContactSchema, status_code=status.HTTP_201_CREATED,
          dependencies=[Depends(RateLimiter(times=2, minutes=5))])
def create_new_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user)
):
    """
    Create a new contact for the current user.
    """
    return crud.create_contact_for_user(db=db, contact=contact, user_id=current_user.id)


@app.get("/contacts/", response_model=List[ContactSchema])
def read_contacts(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of contacts for the current user.
    """
    return crud.get_user_contacts(db, user_id=current_user.id, skip=skip, limit=limit)


@app.get("/contacts/{contact_id}", response_model=ContactSchema)
def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user)
):
    """
    Retrieve a specific contact by ID for the current user.
    """
    contact = crud.get_contact_by_id_for_user(db, contact_id, current_user.id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact