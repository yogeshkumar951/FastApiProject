from fastapi import APIRouter, Depends, HTTPException, UploadFile,File,Form
from sqlalchemy.orm import Session
import schemas, crud, dependencies
from models import User,Roles
from fastapi.responses import JSONResponse
from pathlib import Path

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("")
async def create_user(profilepic: UploadFile = File(...),
        name: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        cellnumber: str = Form(...), 
        roleId: Roles = Form(...), 
        db: Session = Depends(dependencies.get_db), 
        admin: User = Depends(dependencies.get_current_admin)
    ):
    if admin.roleId == 2:
        raise  HTTPException(status_code=403, detail="Admins only")
    roleId = 1 if str(roleId) == 'Roles.ADMIN' else 2
    created_user = await crud.create_user(db,cellnumber, profilepic,name,email,password,roleId)
    return created_user


@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_user(user_id: int, db: Session = Depends(dependencies.get_db), current: User = Depends(dependencies.get_current_admin)):
    if current and current.roleId == 2 and current.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    user_data = await crud.get_user_by_id(db, user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail='User not exist.')
    return user_data


@router.patch("/{user_id}", response_model=schemas.UserResponse)
async def update_user(user_id: int, data: dict, db: Session = Depends(dependencies.get_db), admin: User = Depends(dependencies.get_current_admin)):
    if admin.roleId == 2:
        raise  HTTPException(status_code=403, detail="Admins only")
    updated_user = await crud.update_user(db, user_id, data)
    if not updated_user:
        raise HTTPException(status_code=404, detail='User not exist.')
    return updated_user


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(dependencies.get_db), admin: User = Depends(dependencies.get_current_admin)):
    if admin.roleId == 2:
        raise  HTTPException(status_code=403, detail="Admins only")
    is_delete_intense = await crud.delete_user(db, user_id)
    return {"message": "User deleted"}


@router.get("", response_model=list[schemas.UserResponse])
async def list_users(db: Session = Depends(dependencies.get_db), admin: User = Depends(dependencies.get_current_admin)):
    if admin.roleId == 2:
        raise  HTTPException(status_code=403, detail="Admins only")
    data = await crud.get_all_users(db)
    return data

