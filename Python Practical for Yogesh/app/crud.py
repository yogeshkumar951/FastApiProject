from sqlalchemy.orm import Session
import models, auth
from fastapi import HTTPException
from pathlib import Path


UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

async def create_user(db: Session,cellnumber, profilepic, name, email, password,roleId):
    is_cellnumber_unique = db.query(models.User).filter(models.User.cellnumber == cellnumber).first()
    if is_cellnumber_unique:
        raise HTTPException(status_code=409, detail='CellNumber should be unique.')
    is_email_unique = db.query(models.User).filter(models.User.email == email).first()
    if is_email_unique:
        raise HTTPException(status_code=409, detail='Email should be unique.')
    if roleId not in [1,2]:
        raise HTTPException(status_code=409, detail='Role should be only Admin or User./n Enter 1 for Admin and 2 for User.')
    hashed_pw = auth.encrypt_password(password)
    file_name = await upload_profile(profilepic)
    db_user = models.User(
        name=name,
        profilepic=str(file_name['filename']),
        email=email,
        cellnumber=cellnumber,
        password=hashed_pw,
        roleId=roleId
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def upload_profile(file):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed.")
    
    file_location = UPLOAD_DIR / file.filename
    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)

    return {
        "filename": file.filename,
        "message": "Image uploaded successfully"
    }


async def get_user_by_id(db: Session, user_id: int):
    result = db.query(models.User).filter(models.User.id == user_id).first()
    return result

async def get_all_users(db: Session):
    return db.query(models.User).all()

async def update_user(db: Session, user_id: int, user_data: dict):
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    for key, value in user_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user) 
    return user

async def delete_user(db: Session, user_id: int):
    user = await get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()  
    else:
        raise HTTPException(status_code=404,detail='User not exist.')
