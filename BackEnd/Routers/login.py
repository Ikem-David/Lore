from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from Database.db import get_db
from Database.tables import Users
from auth import create_access_token
from components.hasher import Hash


router = APIRouter(
    prefix="/login",
    tags=["Users","Login"]
)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    # Find user
    user = db.query(Users).filter(
        Users.username == form_data.username
    ).first()

    # User doesn't exist
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # Check password
    if not Hash.verify_password(
        form_data.password,
        user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # Create JWT
    access_token = create_access_token(
        data={
            "sub": user.username
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }