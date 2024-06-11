from datetime import datetime, timedelta, timezone
from typing import Annotated
import os
import logging

from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


from jose import JWTError, jwt

from starlette.middleware.sessions import SessionMiddleware

from sqlalchemy.orm import Session

from . import schemas, crud, views
from .router import auth_router
from .settings import settings
from .verification import send_verification_signup
from .templates import template_env
from .startup import startup
from .models import User
from .pub import logged_in_user
from . import views

__version__ = '0.0.8'

# suppress AttributeError: module 'bcrypt' has no attribute '__about__'
logging.getLogger('passlib').setLevel(logging.ERROR)

# startup(auth_router)


def package_path():
    return os.path.dirname(__file__) # .replace("simpleauth/__init__.py", "")


startup()


class SimpleAuth():
    def __init__(self, app: FastAPI):
        self.app = app
        self.register()

    def register(self):
        self.app.add_middleware(SessionMiddleware, secret_key='ChangeMe', max_age=None)
        self.app.include_router(auth_router, prefix="/auth")
        self.app.mount("/auth/static", 
                       StaticFiles(packages=[settings.template_theme]), 
                       name="simpleauth-static")



def __main__():
    pass
