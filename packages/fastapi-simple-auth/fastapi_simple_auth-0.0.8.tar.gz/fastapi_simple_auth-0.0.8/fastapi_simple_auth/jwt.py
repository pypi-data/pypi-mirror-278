# jwt.py
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from .settings import settings
from .models import User
from . import crud


ALGORITHM = "HS256"

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)




def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt

def make_tokens(user: User) -> dict:

    tokens = dict()

    data = {
        "sub": user.uuid,
        "username": user.username
        }

    access_token_expires = timedelta(seconds=settings.access_token_expire)
    access_token = create_token(
        data={**data, 'type': 'access'}, expires_delta=access_token_expires
    )

    tokens['access_token'] = access_token

    if settings.refresh_token_expire:
        refresh_token_expires = timedelta(seconds=settings.refresh_token_expire)
        refresh_token = create_token(
            data={**data, 'type': 'refresh'}, expires_delta=refresh_token_expires
        )
        tokens['refresh_token'] = refresh_token

    return tokens

def jwt_payload(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception
    return payload
    

def get_current_user_bearer(request: Request, db: Session):
    
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None

    try:
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            return None
    except ValueError:
        return None

    payload = jwt_payload(token)

    if payload.get('type') != 'access':
        raise credentials_exception

    user = crud.get_user_by_uuid(db, uuid=payload['sub'])
    return user
