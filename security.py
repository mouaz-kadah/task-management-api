from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi import Header, HTTPException

SECRET_KEY = "your-secret-key-change-this"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except jwt.InvalidTokenError:
        return None

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token مفقود")
    
    # استخرج الـ token من "Bearer TOKEN"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Token format غلط")
    
    token = parts[1]
    username = decode_token(token)
    
    if username is None:
        raise HTTPException(status_code=401, detail="Token غلط أو انتهى")
    
    return username