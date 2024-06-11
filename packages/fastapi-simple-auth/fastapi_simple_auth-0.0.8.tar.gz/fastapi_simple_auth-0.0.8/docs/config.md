# Configuration settings

Configuration settings are defined in settings.py and should be configured either using environment variables
or using .env file

## Application
### APP_TITLE
title of application, default: "My Noname App"

### SECRET_KEY
random secret key. generate it with python:
~~~
"".join(random.choices(string.ascii_letters + string.digits, k=50))
~~~

or from this shell one-lines:
~~~
< /dev/urandom tr -dc '[:alnum:]_$#%-' | head -c50; echo
~~~


## Database
### DB_URL
Address of database, default: `sqlite:///./test.db`

## Authentication

### AUTH_TRANSPORT
default: "session"

Where we hold successful authentication

### USERNAME_IS_EMAIL
If `True`, all usernames must be email addresses (e.g. batman2000@hotmail.com) and will be verified.
If `False`, usernames are just strings (e.g. batman2000) and not verified


### TRANSPORT_SESSION
Boolean, If `True`, session transport is enabled. (authentication is held in session)

### TRANSPORT_BEARER
Boolean, If `True`, JWT bearer token transport is enabled.

## Code generation
Recovery and verification codes are generated based on these settings:
~~~
    code_size: int = 6
    code_set: str = "digits"
    code_lifetime: int = 86400
    code_regenerate: int = 30
~~~


## Sending mail
~~~python3
    mail_transport: str = "stdout"
    mail_host: str = "127.0.0.1"
    mail_port: int = 25
    mail_from: str = "NoReply <noreply@example.com>"
    mail_user: str | None = None
    mail_password: str | None = None
    mail_starttls: bool = False
~~~

## Cron
~~~
    cron_interval: int = 300
~~~

## Navigation
~~~
    afterlogin_url: str = "/"
    afterlogout_url: str = "login"
    ### redirect to login if not authenticated
    notauth_login: bool = True

    # authenticate automatically after signup
    signin_after_signup: bool = True
~~~

## Themes
### TEMPLATE_THEME 
Name of template theme package. Default: fastapi_simple_auth_basic

## Password requirements

### PASSWORD_ZXCVBN
[ZXCVBN](https://github.com/dwolfhub/zxcvbn-python) minimal password score (integer, from 0 to 4).

### PASSWORD_STRENGTH_POLICY
Space-separated key=value list for [py-password-strength](https://github.com/kolypto/py-password-strength), example: `length=8 uppercase=1 numbers=1 special=1 nonletters=3 entropybits=20 strength=0.66`



