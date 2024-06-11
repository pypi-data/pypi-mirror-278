from fastapi import FastAPI

from fastapi_simple_auth import SimpleAuth, logged_in_user
from fastapi_simple_auth.views import User
        
app = FastAPI()

simpleauth = SimpleAuth(app)

@app.get("/", response_model=User)
async def read_users_me(
    # user: logged_in_user
    user: logged_in_user
):
    return user
