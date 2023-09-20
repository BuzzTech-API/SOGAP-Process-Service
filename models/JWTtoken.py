from fastapi import HTTPException, status
from jose import JWTError, jwt

from datetime import datetime, timedelta
from typing import Annotated, Any, Union
from models import user_crud, JWTtoken
from database.schemas import TokenData
import os
from dotenv import dotenv_values

# Python Environment Variable setup required on System or .env file
config_env = {
    **dotenv_values(".env"),  # load local file development variables
    **os.environ,  # override loaded values with system environment variables
}



ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 2 # 2 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = config_env['JWT_SECRET_KEY']   # should be kept secret
JWT_REFRESH_SECRET_KEY = config_env['JWT_REFRESH_SECRET_KEY']   # should be kept secret


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Realiza a criação do token de autenticação"""
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception, db):
    """Verifica se aquele token é verdadeiro"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('sub')
        if email is None:
            raise credentials_exception
        if datetime.fromtimestamp(payload.get('exp')) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise credentials_exception
    user = user_crud.get_user_by_email(db=db, email=email)
    if user is None:
        raise credentials_exception
    return user


def create_refresh_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expires_delta})
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def refresh_token(token: str, credentials_exception, db):
    """Verifica se aquele token é verdadeiro"""
    try:
        payload = jwt.decode(token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('sub')
        if email is None:
            raise credentials_exception
        if datetime.fromtimestamp(payload.get('exp')) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise credentials_exception
    user = user_crud.get_user_by_email(db=db, email=email)
    if user is None:
        raise credentials_exception
    
    access_token = JWTtoken.create_access_token(
        data={"sub": user.email}
    )
    refresh_token = JWTtoken.create_refresh_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "refresh_token":refresh_token, "token_type": "bearer"}