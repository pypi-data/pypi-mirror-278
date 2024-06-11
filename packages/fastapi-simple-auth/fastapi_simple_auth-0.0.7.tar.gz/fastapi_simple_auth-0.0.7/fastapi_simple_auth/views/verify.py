import datetime

from pydantic import EmailStr

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..router import auth_router
from ..db import get_db
from ..templates import template_env
from ..settings import settings
from ..verification import get_code_record, resend_verification
from ..cron import cron


@auth_router.get('/emailverify/{email}')
def get_email_verify(rq: Request, email: EmailStr, code: str = "", db: Session = Depends(get_db)):
    error = None
    verify = True
    resend = True

    # get code record
    user = crud.get_user_by_username(db=db, username=email)
    if user is None:
        error = f'User {email} does not exist!'
        verify = False
        resend = False

    code_rec = get_code_record(db=db, user=user)
    msg = None
    if code_rec:
        msg = f'Message to {user.username} was sent at {code_rec.created}'

        # if code age is older than settings.code_regenerate
        if not code_rec.can_resend():
            verify = True
            resend = False

    else:
        error = f'No code found for {email}'
        verify = False
        resend = False


    tpl = template_env.get_template('verify-email.html')
    ctx = {
        "rq": rq,
        "settings": settings,
        "email": email,
        "message": msg,
        "error": error,
        "verify": verify,
        "resend": resend,
        "code": code,
    }

    html = tpl.render(ctx)
    return HTMLResponse(html)

@auth_router.post('/emailverify/{email}')
def email_verify_post(rq: Request, email: EmailStr, coderq: schemas.VerificationCode, db: Session = Depends(get_db)):
    
    resp_bad = Response(status_code=400, content="Bad code")
    
    user = crud.get_user_by_username(db=db, username=email)    
    code = get_code_record(db=db, user=user, code=coderq.code)

    if not code:
        return resp_bad
    
    cron(db)

    if code.purpose == 'signup':
        user.email_verified = True
        success = {
                'text': 'Verification successful! You can login now!',
                'url': str(rq.url_for('get_login'))
            }

    elif code.purpose == 'change_email':
        user.email = email
        success = {
                'text': f'Your email changed. You can login as {email} now!',
                'url': str(rq.url_for('get_login'))
            }

    db.delete(code)
    db.commit()
    return success

@auth_router.post('/emailverify_resend/{email}')
def email_verify_resend(rq: Request, email: EmailStr, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db=db, username=email)    
    code = get_code_record(db=db, user=user)

    cron(db)

    if not user:
        return Response(status_code=400, content="User does not exist")
    
    if not code:
        return Response(status_code=400, content="Code does not exist")
    
    if not code.can_resend():        
        return Response(status_code=429, content="Cannot resend now")
    
    resend_verification(rq=rq, db=db, user=user, code=code)
    return Response(status_code=200, content=f"Code resent to {user.username}")




