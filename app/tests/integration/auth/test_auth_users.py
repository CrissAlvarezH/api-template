from typing import Tuple

from jose import jwt

from app.auth.utils import authenticate_user
from app.auth.models import User
from app.auth.schemas import TokenData
from app.auth.utils import get_password_hash, create_access_token
from app.core.config import settings


def create_sample_user(db) -> Tuple[User, str]:
    password = "userpass1234"
    user = User(
        full_name="Cristian Alvarez",
        email="cristian@email.com",
        password=get_password_hash(password),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user, password


def test_authenticate_user(db):
    user, password = create_sample_user(db)

    auth_user = authenticate_user(db, user.email, password)

    assert auth_user.id == user.id
    assert auth_user.full_name == user.full_name
    assert auth_user.email == user.email


def test_create_access_token(db):
    user, _ = create_sample_user(db)

    access_token = create_access_token(TokenData(user=user))

    decoded = jwt.decode(
        access_token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM
    )

    assert decoded.get("user").get("id") == user.id
    assert decoded.get("user").get("full_name") == user.full_name
    assert decoded.get("user").get("email") == user.email
