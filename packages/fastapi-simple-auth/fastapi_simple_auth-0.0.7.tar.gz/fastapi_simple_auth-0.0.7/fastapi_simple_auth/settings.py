from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import string
import random



# generate random secret key
default_secret_key = "".join(random.choices(string.ascii_letters + string.digits, k=50))

class Settings(BaseSettings):
    db_url: str = "sqlite:///./test.db"

    app_title: str = "My Noname App"
    secret_key: str = default_secret_key

    login_result: str = "session"
    
    # Unused. if username_is_email, verification is enabled
    # email_verification: bool = False
    
    username_is_email: bool = True

    code_size: int = 6
    code_set: str = "digits"
    code_lifetime: int = 86400
    code_regenerate: int = 30

    access_token_expire: int = 0
    refresh_token_expire: int = 0
    
    mail_transport: str = "stdout"
    mail_host: str = "127.0.0.1"
    mail_port: int = 25
    mail_from: str = "NoReply <noreply@example.com>"
    mail_user: str | None = None
    mail_password: str | None = None
    mail_starttls: bool = False

    transport_bearer: bool = True
    transport_session: bool = True

    cron_interval: int = 300

    afterlogin_url: str = "/"
    afterlogout_url: str = "login"
    
    # redirect to login if not authenticated
    notauth_login: bool = True

    # authenticate automatically after signup
    signin_after_signup: bool = True

    password_zxcvbn: int | None = None 
    password_strength_policy: str | None = None

    template_theme: str = "fastapi_simple_auth_basic"

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

settings = Settings()
