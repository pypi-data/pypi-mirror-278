import json

from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse

from ..router import auth_router
from ..settings import settings

@auth_router.get('/settings.js')
def settings_view(rq: Request):
    
    path_parts = rq.url.path.split('/')
    path = '/'.join(path_parts[:-1])


    data = {
        'base_url': path,
        'username_is_email': settings.username_is_email,
        'signin_after_signup': settings.signin_after_signup,
        'afterlogin_url': settings.afterlogin_url,
        'afterlogout_url': settings.afterlogout_url
    }
    
    js_content = f"""
    const settings = {json.dumps(data)};
    sessionStorage.setItem("simpleAuthSettings", JSON.stringify(settings));
    """

    response = Response(content=js_content, media_type="application/javascript")

    return response
