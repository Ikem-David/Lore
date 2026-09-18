from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Database.db import get_db
from Database.tables import Users
from Schema import users
from auth import create_access_token
from components.hasher import Hash


router = APIRouter(
    prefix="/login",
    tags=["Users","Login"]
)


@router.post("/login")
def login(
    req: users.LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(Users).filter(
        Users.email == req.email
    ).first()

    # User doesn't exist
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # Check password
    if not Hash.verify_password(
        req.password,
        user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # Create JWT
    access_token = create_access_token(
        data={
            "sub": user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }