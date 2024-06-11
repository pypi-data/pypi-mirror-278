# API testing

## Create user
~~~
http POST http://localhost:8000/auth/users/ username=u1@example.com password=MyPassword
~~~

## Login (session)
~~~
http --session=test -f http://localhost:8000/auth/login username=u1@example.com password=MySecret
~~~

## Login (JWT)
~~~
http --session=test -f POST http://localhost:8000/auth/jwt/get username=u1@example.com password=MySecret
~~~

## Refresh token (JWT)
~~~
export REFRESH=eyJ...
http -A bearer -a $REFRESH POST http://localhost:8000/auth/jwt/refresh
~~~

## Change Password
~~~
http --session=test http://localhost:8000/auth/change_password old_password=MySecret password=MyNewSecret
~~~

## Get JWT