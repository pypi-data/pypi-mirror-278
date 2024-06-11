import uuid
import datetime

from sqlalchemy import Boolean, Integer, Column, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from passlib.context import CryptContext

from .settings import settings

Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def get_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    uuid = Column(String(36), nullable=False, unique=True, primary_key=True, default=get_uuid)
    # username may be also email
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created = Column(DateTime)
    last_login = Column(DateTime)
    admin_comment = Column(String)
    email_verified = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)
    other = Column(Text)
    codes = relationship("Code", back_populates="user")

    def __repr__(self):
        return f"user {self.uuid} {self.username}"

    def dump(self):
        return f"username: {self.username}\n" \
            f"uuid: {self.uuid}\n" \
            f"verified: {self.email_verified}\n" \
            f"codes: {' '.join([ c.code for c in self.codes]) }"

    def set_password(self, new_password: str):
        self.password = get_password_hash(new_password)

class Code(Base):
    __tablename__ = "codes"

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)

    user_id = Column(String(36), ForeignKey("users.uuid"), nullable=True)    
    code = Column(String)
    # argument: email
    argument = Column(String)
    # purpose: signup, change_email, recover
    purpose = Column(String)
    created = Column(DateTime(timezone=True), server_default=func.now())
    expires = Column(DateTime(timezone=True))
    user = relationship("User", back_populates="codes")

    def can_resend(self):
        # get UTC time, but make it naive, because sqlite returns naive
        now = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
        return now > self.created + datetime.timedelta(seconds=settings.code_regenerate)

    def __repr__(self):
        return f"{self.user} {self.purpose}({self.argument}) {self.code} {self.created}"