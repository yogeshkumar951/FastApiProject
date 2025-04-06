import sys
from models import User
import auth
from database import SessionLocal
from fastapi import  HTTPException


def main():
    command = sys.argv[1]
    db = SessionLocal()
    if command == "create_admin":
        username = input('Enter name :')
        email = input('Enter email :')
        cellnumber = input('Enter cellnumber :')
        password = input('Enter password :')
        hashed_pw = auth.encrypt_password(password)

        is_cellnumber_unique = db.query(User).filter(User.cellnumber == cellnumber).first()
        if is_cellnumber_unique:
            raise HTTPException(status_code=409, detail='CellNumber should be unique.')
        
        is_email_unique = db.query(User).filter(User.email == email).first()
        if is_email_unique:
            raise HTTPException(status_code=409, detail='Email should be unique.')

        db_user = User(
            name = username,
            profilepic = '',
            email = email,
            cellnumber = cellnumber,
            password = hashed_pw,
            roleId = 1 
        )
        db.add(db_user)
        db.commit()
        print('Admin user created.')
   

if __name__ == "__main__":
    main()