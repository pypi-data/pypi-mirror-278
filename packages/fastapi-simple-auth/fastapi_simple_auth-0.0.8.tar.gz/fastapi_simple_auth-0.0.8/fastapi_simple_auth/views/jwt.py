
from typing import Annotated
from datetime import timedelta, datetime, timezone
from fastapi import Depends, FastAPI, APIRouter, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from jose import JWTError, jwt

from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
# import Invalid

from ..db import get_db
from ..router import auth_router
from ..settings import settings
from ..models import User
from ..jwt import credentials_exception, make_tokens, jwt_payload
from .. import crud


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/jwt/get")

@auth_router.post("/jwt/get")
def get_jwt_token(
        rq: Request, 
        form: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)):

    tokens = dict()

    if not settings.access_token_expire:
        # disabled
        return None

    # here is POST
    user = crud.get_auth_user(db, form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    tokens = make_tokens(user)

    return tokens

@auth_router.post("/jwt/refresh")
def refresh_jwt_token(
        rq: Request, 
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db)):

    payload = jwt_payload(token)

    if payload.get('type') != 'refresh':
        raise credentials_exception

    user = crud.get_user_by_uuid(db, uuid=payload['sub'])

    tokens = make_tokens(user)
    return tokens

