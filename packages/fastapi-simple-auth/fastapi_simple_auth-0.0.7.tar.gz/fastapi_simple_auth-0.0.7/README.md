# FastAPI Simple Auth

- Such a long name! It's hard to type it out.
- Yes, but everything else in this project is simple.

## Authentication easy as three lines!

1. Import package
2. hook to app with `SimpleAuth(app)`
3. add `user: logged_in_user` to protected view

~~~python
from fastapi import FastAPI
from fastapi_simple_auth import SimpleAuth, logged_in_user
        
app = FastAPI()

simpleauth = SimpleAuth(app)

@app.get("/")
async def read_users_me(user: logged_in_user) -> str:    
    return f"Hello {user.username} {user.uuid}"
~~~

![login screenshot](docs/docs/img/login.png)

## Features
- Users are stored in any supported SQLAlchemy database
- Optional email verification
- User creation
- Password recovery
- Profile page with change password, change email
- Custom UI themes!


## Install

~~~shell
pip3 install fastapi-simple-auth
# create/edit .env file
vim .env
simpleauth dbupgrade
~~~

Write app in app.py

Start:
~~~
uvicorn app:app
~~~


## Usage

This examples uses [httpie](http://httpie.io/) because it is very good to craft JSON requests.

~~~
# register
http POST http://localhost:8000/auth/users/ username=me@example.com password=secret

# simple auth (session)
http -f POST http://localhost:8000/auth/login username=me@example.com password=secret

# get token
http -f POST http://localhost:8000/auth/token username=me@example.com password=secret
~~~

## Developer cheatsheet
### Alembic cheatsheet
~~~
alembic revision --autogenerate -m "some desc"
alembic upgrade head
alembic current
~~~