import os
from datetime import datetime
from typeing import Union, Any
from passlib.context import CryptContext
from jose import jwt

## Constants
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFERESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_REFERSH_SECRET_KEY = os.environ.get("JWT_REFERSH_SECRET_KEY")

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordHandler():
    def get_password_hash(self, password):
        return password_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return password_context.verify(plain_password, hashed_password)

class TokenHandler():
    def create_access_token(self, data: dict, expires_delta: Union[datetime, None] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return encoded_jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    
    def create_refersh_token(self, subject: Union[str, Any], expires_delta: Union[datetime, None] = None):
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
        return encoded_jwt