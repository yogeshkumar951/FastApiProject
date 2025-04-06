import bcrypt
import uuid
from datetime import datetime
from models import AccessToken
from sqlalchemy.orm import Session
import os

def encrypt_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode())

def create_token(db: Session, user_id: int):
    token = uuid.uuid4().hex
    ttl = os.getenv('TOKEN_EXPIRE_TIME')
    new_token = AccessToken(token=token, ttl=ttl, userId=user_id, created=datetime.now())
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return new_token
