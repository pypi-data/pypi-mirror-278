from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, Request
from .settings import settings
from .crud import get_user_by_uuid
from sqlalchemy.orm import Session

def session_startup(app: FastAPI):
    app.add_middleware(SessionMiddleware, secret_key=settings.secret_key, max_age=None)

def get_current_user_session(request: Request, db: Session):
    try:
        uuid = request.session['user']
    except KeyError:
        return None
    
    user = get_user_by_uuid(db, uuid)
    return user

