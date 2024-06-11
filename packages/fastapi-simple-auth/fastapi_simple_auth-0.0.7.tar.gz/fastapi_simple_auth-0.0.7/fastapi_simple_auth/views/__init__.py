
import json
from typing import Annotated
from pydantic import BaseModel, EmailStr

from fastapi import Request, Response, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from ..router import auth_router
from ..templates import template_env
from ..settings import settings

from .. import crud, schemas
from ..db import get_db
from ..exceptions import SimpleAuthVerificationAlreadySent
from ..cron import cron

from . import login, profile, settingsjs, signup, verify, recover, jwt

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    disabled: bool | None = None

