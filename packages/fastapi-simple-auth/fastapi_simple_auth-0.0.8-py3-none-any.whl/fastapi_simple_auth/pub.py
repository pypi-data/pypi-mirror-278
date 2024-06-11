from typing import Annotated
from fastapi import Depends, HTTPException, Request 
from .settings import settings
from . import views
from sqlalchemy.orm import Session
from .db import get_db
from .session import get_current_user_session
from .jwt import get_current_user_bearer
from .models import User
# public interface


async def get_current_user(request: Request, db: Session = Depends(get_db)): 
    if settings.transport_session:
        user = get_current_user_session(request, db)

    if user:
        return user

    if settings.transport_bearer:
        user = get_current_user_bearer(request, db)

    return user

async def get_current_active_user(
        rq: Request,
        user: Annotated[User, Depends(get_current_user)],
):

    if user is None:
        if settings.notauth_login:
            raise HTTPException(status_code=302, detail="Not authorized", 
                            headers = {"Location": str(rq.url_for('get_login'))} )
        else:
            raise HTTPException(status_code=403)

    return user

logged_in_user = Annotated[User, Depends(get_current_active_user)]
