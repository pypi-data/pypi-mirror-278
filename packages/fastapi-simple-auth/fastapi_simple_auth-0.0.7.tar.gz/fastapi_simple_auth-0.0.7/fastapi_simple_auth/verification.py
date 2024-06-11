from .settings import settings
from .templates import template_env
from .models import User, Code
from .envmail import send_mail

from fastapi import Request
from pydantic import EmailStr

import string
import random
import datetime

from sqlalchemy.orm import Session

codesets = {
    "digits": string.digits,
    "lower": string.ascii_lowercase,
    "upper": string.ascii_uppercase,
    "letters": string.ascii_letters
}

def generate_code():
    try:
        codeset = codesets[settings.code_set]
    except KeyError as e:
        raise KeyError(f'CODE_SET must be one of: { " ".join(codesets) }')

    code = ''.join(random.choice(codeset) for i in range(settings.code_size))
    return code


def create_code_record(db: Session, user: User, purpose: str, seconds: int, argument: str | None = None) -> Code:
    code_value = generate_code()
    expires = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    
    print("create_code_record code:", code_value)
    code_record = Code(
        code=code_value, 
        user=user,
        purpose=purpose,
        argument=argument, 
        expires=expires)
    db.add(code_record)
    db.commit()
    return code_record

def get_code_record(db: Session, user: User, code: str = None):
    if code is None:
        return db.query(Code).filter(Code.user == user).first()
    
    return db.query(Code).filter(Code.user == user, Code.code == code).first()


def send_verification_signup(rq: Request, db: Session, user: User):
    email = user.username
    cr = create_code_record(db=db, user=user, purpose='signup', seconds=settings.code_lifetime)
    tpl = template_env.get_template('email/confirm-email.html')
    html = tpl.render(rq =rq, code = cr.code, title = settings.app_title, email = email)
    send_mail(email, subject=f"Registration on {settings.app_title}", html=html)

def send_verification_change_email(rq: Request, db: Session, user: User, email: EmailStr):    
    cr = create_code_record(db=db, user=user, purpose='change_email', seconds=settings.code_lifetime, argument=email)
    tpl = template_env.get_template('email/change-email.html')
    html = tpl.render(rq = rq, code = cr.code, title = settings.app_title, email = email)    
    send_mail(email, subject=f"Change email address on {settings.app_title}", html=html)

def send_recovery_email(rq: Request, db: Session, user: User):
    email = user.username
    cr = create_code_record(db=db, user=user, purpose='recover', seconds=settings.code_lifetime)
    tpl = template_env.get_template('email/recover.html')
    html = tpl.render(rq = rq, code = cr.code, title = settings.app_title, email = email)
    send_mail(email, subject=f"Recover password on {settings.app_title}", html=html)

def resend_verification(rq: Request, db: Session, user: User, code: Code):
    print("resend verification", code)
    db.delete(code)    

    if code.purpose == 'signup':
        send_verification_signup(rq=rq, db=db, user=user)

    elif code.purpose == 'change_email':
        send_verification_change_email(rq=rq, db=db, user=user, email=code.argument)

    elif code.purpose == 'recover':
        send_recovery_email(rq=rq, db=db, user=user)
