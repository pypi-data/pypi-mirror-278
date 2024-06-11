from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session
from pydantic import EmailStr, BaseModel

from .. import crud
from ..router import auth_router
from ..db import get_db
from ..settings import settings
from ..templates import template_env
from ..verification import get_code_record, send_recovery_email
from ..cron import cron

@auth_router.get('/recover')
def get_recover(rq: Request, db: Session = Depends(get_db)):
    tpl = template_env.get_template('recover.html')
    ctx = {
        'rq': rq,
        'settings': settings
    }

    html = tpl.render(ctx)
    return HTMLResponse(html)

class RecoverRq(BaseModel):
    email: EmailStr

@auth_router.post('/recover')
def post_recover(rq: Request, recoverrq: RecoverRq, db: Session = Depends(get_db)):
    
    # always same response to avoid username enumeration
    r = Response("If such user exists, we sent recovery email. Please check your inbox.")

    email = recoverrq.email
    user = crud.get_user_by_username(db=db, username=email)
    if user is None:
        return r

    code_rec = get_code_record(db=db, user=user)
    if code_rec and not code_rec.can_resend():
        return r
    
    send_recovery_email(rq=rq, db=db, user=user)

    return r

@auth_router.get('/recover/{email}')
def get_recover_code(rq: Request, email:EmailStr, code: str = "", db: Session = Depends(get_db)):
    tpl = template_env.get_template('recover_code.html')
    ctx = {
        'rq': rq,
        'settings': settings,
        'code': code
    }

    html = tpl.render(ctx)
    return HTMLResponse(html)

class RecoverSetPassRq(BaseModel):
    code: str
    password: str

@auth_router.post('/recover/{email}')
def post_recover_code(rq: Request, email:EmailStr, setpassrq: RecoverSetPassRq, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db=db, username=email)    
    code = get_code_record(db=db, user=user, code=setpassrq.code)

    resp_bad = Response(status_code=400, content="Invalid code")

    if not code:
        return resp_bad
    
    cron(db)
    crud.change_password(db=db, user=user, new_password=setpassrq.password)
    db.delete(code)
    db.commit()
    return Response()


