from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import SessionLocal
from models import AccessToken, User
from datetime import datetime, timedelta
from typing import Optional
import auth

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_admin(cellnumber: str = Header(...),password:str=Header(...), db: Session = Depends(get_db)):
    is_admin = db.query(User).filter(User.cellnumber == cellnumber).first()
    admin_user = None
    if is_admin and is_admin.roleId==1 and auth.verify_password(password, is_admin.password):
        return is_admin
    elif is_admin and is_admin.roleId==2 and auth.verify_password(password, is_admin.password):
        return is_admin
    else:
        raise HTTPException(status_code=403, detail="Admins only")


