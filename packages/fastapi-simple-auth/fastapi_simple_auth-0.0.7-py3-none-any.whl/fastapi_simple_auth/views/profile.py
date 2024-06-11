from pydantic import BaseModel, EmailStr
from fastapi import Request, Response, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ..router import auth_router
from ..templates import template_env
from ..settings import settings
from ..pub import logged_in_user
from ..crud import verify_password, get_password_hash, change_password
from ..db import get_db
from ..verification import send_verification_change_email
from ..passwordstrength import PasswordStrengthError, check_password


@auth_router.get('/profile')
def profile_get(request: Request, user: logged_in_user, response_class=HTMLResponse):
    tpl = template_env.get_template('profile.html')

    ctx = {
        'rq': request,
        'settings': settings,
        'user': user,
    }

    html = tpl.render(ctx)
    return HTMLResponse(html)

class ChangePasswordModel(BaseModel):
    old_password: str
    password: str


@auth_router.post('/change_password')
def change_pass_post(request: Request, user: logged_in_user, 
                     chpass: ChangePasswordModel,
                     db: Session = Depends(get_db)):

    if not verify_password(chpass.old_password, user.password):
        return Response(status_code=401, content="Wrong password")

    try:
        check_password(chpass.password)
    except PasswordStrengthError as e:
        return Response(status_code=401, content=str(e))



    change_password(db=db, user=user, new_password=chpass.password)

    return Response('password changed')

class ChangeEmailModel(BaseModel):
    email: EmailStr

@auth_router.post('/change_email')
def change_email_post(request: Request, user: logged_in_user, 
                     mail: ChangeEmailModel,
                     db: Session = Depends(get_db)):

    send_verification_change_email(rq=request, db=db, user=user, email=mail.email)

    return Response('confirmation email sent')

