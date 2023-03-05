from typing import Optional, List

from sqlalchemy.orm import Session

from app.auth.models import User, Scope, UserScope
from app.auth.schemas import UserCreate, UserUpdate
from app.auth.utils import get_password_hash


def get_user_by_id(db: Session, _id: int) -> Optional[User]:
    return db.query(User).filter(User.id == _id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def list_users(db: Session) -> List[User]:
    return db.query(User).all()


def create_user(db: Session, obj_in: UserCreate) -> User:
    user = User(
        full_name=obj_in.full_name,
        email=obj_in.email,
        password=get_password_hash(obj_in.password),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_scope(db: Session, scope_name: str) -> Optional[Scope]:
    return db.query(Scope).filter(Scope.name == scope_name).first()


def list_scopes(db: Session) -> List[Scope]:
    return db.query(Scope).all()


def create_scope(db: Session, scope_name: str) -> Scope:
    scope = Scope(name=scope_name)
    db.add(scope)
    db.commit()
    db.refresh(scope)
    return scope


def add_scope_to_user(db: Session, user_id: int, scope: str):
    if not get_scope(db, scope):
        raise ValueError("scope doesn't exists")
    user_scope = UserScope(user_id=user_id, scope_name=scope)
    db.add(user_scope)
    db.commit()


def remove_all_scopes(db: Session, user_id: int):
    db.query(UserScope).filter(UserScope.user_id == user_id).delete()
    db.commit()


def update_user(db: Session, _id: int, obj_in: UserUpdate) -> User:
    user = get_user_by_id(db, _id)
    if not user:
        raise ValueError("doesn't exist user")

    if obj_in.full_name:
        user.full_name = obj_in.full_name
    if obj_in.scopes:
        remove_all_scopes(db, _id)
        for scope in obj_in.scopes:
            add_scope_to_user(db, _id, scope)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
