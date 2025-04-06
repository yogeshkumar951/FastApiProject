from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, models, auth, dependencies

router = APIRouter(prefix="/api/users", tags=["login"])

@router.post("/login", response_model=schemas.TokenResponse)
async def login(request: schemas.LoginRequest, db: Session = Depends(dependencies.get_db)):
    user = db.query(models.User).filter(models.User.cellnumber == request.cellnumber).first()
    if (user and not auth.verify_password(request.password, user.password)) or not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if user.roleId == 1:
        raise HTTPException(status_code=401, detail="Normal users only")
    return auth.create_token(db, user.id)
