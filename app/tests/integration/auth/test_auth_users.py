from jose import jwt

from app.auth.utils import authenticate_user
from app.auth.schemas import TokenData
from app.auth.utils import create_access_token
from app.core.config import settings

from app.tests.factories import UserFactory


def test_authenticate_user(db):
    user, password = UserFactory.sample_user(db)

    auth_user = authenticate_user(db, user.email, password)

    assert auth_user.id == user.id
    assert auth_user.full_name == user.full_name
    assert auth_user.email == user.email

    db.delete(user)
    db.commit()


def test_create_access_token(db):
    user, _ = UserFactory.sample_user(db)

    access_token = create_access_token(TokenData(user=user))

    decoded = jwt.decode(
        access_token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM
    )

    assert decoded.get("user").get("id") == user.id
    assert decoded.get("user").get("full_name") == user.full_name
    assert decoded.get("user").get("email") == user.email

    db.delete(user)
    db.commit()
