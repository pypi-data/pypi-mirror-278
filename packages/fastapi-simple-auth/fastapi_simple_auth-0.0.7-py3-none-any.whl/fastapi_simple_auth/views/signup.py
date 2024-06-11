from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from .. import schemas, crud
from ..settings import settings
from ..router import auth_router
from ..templates import template_env
from ..db import get_db
from ..verification import send_verification_signup
from ..exceptions import SimpleAuthVerificationAlreadySent
from ..passtr import PasswordStrengthError, check_password

@auth_router.get('/signup')
def get_signup(request: Request, response_class=HTMLResponse):
    tpl = template_env.get_template('register.html')

    ctx = {
        'rq': request,
        'settings': settings,
        'motd2': 'motd motd motd motd motd motd',
        'error2': 'some problem'
    }

    html = tpl.render(ctx)
    return HTMLResponse(html)


@auth_router.post("/users/") # , response_model=schemas.User)
def create_user(rq: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    db_user = crud.get_user_by_username(db, username=user.username)

    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")


    try:
        check_password(user.password)
    except PasswordStrengthError as e:
        raise HTTPException(status_code=400, detail=str(e))


    user = crud.create_user(db=db, user=user)
    if settings.username_is_email:
        try:
            send_verification_signup(rq=rq, db=db, user=user)
            return {"status": "OK", 
                    "message": "Please check your email for verification code",
                    "redirect": str(rq.url_for("get_email_verify", email=user.username))
                    }
        
        except SimpleAuthVerificationAlreadySent as e:
            print("ERR", e)
    else:
        print("created user", user)    
        if settings.signin_after_signup:
            # authenticate user
            if settings.auth_transport == "session":
                rq.session['user'] = user.uuid        
                return {"status": "OK", 
                        "redirect": settings.afterlogin_url }
        else:
            return {"status": "OK", 
                    "message": "Please check your email for verification code",
                    "redirect": settings.afterlogin_url }

    
    print("return")
    # return user
    return Response()
