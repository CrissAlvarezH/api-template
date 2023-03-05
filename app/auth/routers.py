from typing import List

from fastapi import APIRouter, HTTPException, status, Depends, Body, Security, Path
from fastapi.security import OAuth2PasswordRequestForm

from app.db.dependencies import get_db

from app.auth import schemas, crud
from app.auth.utils import authenticate_user, create_access_token
from app.auth.dependencies import Auth
from app.auth.scopes import LIST_USERS, EDIT_USERS


router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=schemas.Token)
async def login(
    db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials",
        )

    access_token = create_access_token(schemas.TokenData(user=user))
    return schemas.Token(access_token=access_token)


@router.post("/register", response_model=schemas.Token)
async def register(db=Depends(get_db), user_in: schemas.UserCreate = Body()):
    # check email is not taken
    if crud.get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email is taken"
        )

    # if not taken the email, then create user
    user_created = crud.create_user(db, user_in)
    access_token = create_access_token(schemas.TokenData(user=user_created))

    return schemas.Token(access_token=access_token)


@router.get(
    "/users",
    response_model=List[schemas.UserRetrieve],
    dependencies=[Security(Auth, scopes=[LIST_USERS])],
)
async def user_list(db=Depends(get_db)):
    return crud.list_users(db)


@router.put(
    "/users/{user_id}/",
    response_model=schemas.UserRetrieve,
    dependencies=[Security(Auth, scopes=[EDIT_USERS])],
)
async def user_edit(
    db=Depends(get_db),
    user_id: int = Path(),
    user_in: schemas.UserUpdate = Body(),
):
    try:
        user = crud.update_user(db, user_id, user_in)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
