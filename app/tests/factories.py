from typing import Tuple, Union, List, Optional

from faker import Faker

from app.auth.models import User, UserScope, Scope
from app.auth.utils import get_password_hash


class UserFactory:
    @classmethod
    def sample_user(cls, db, scopes: Optional[List[str]] = None) -> Tuple[User, str]:
        if scopes is None:
            scopes = []

        user_data = cls.random_user_data()

        user = User(
            full_name=user_data.get("full_name"),
            email=user_data.get("email"),
            password=get_password_hash(user_data.get("password")),
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        for scope in scopes:
            user_scope = UserScope(user_id=user.id, scope_name=scope)
            db.add(user_scope)
            db.commit()

        return user, user_data.get("password")

    @classmethod
    def create_scopes(cls, db, scopes: List[str]):
        for s in scopes:
            scope_in_db = db.query(Scope).filter(Scope.name == s).first()
            if scope_in_db:
                continue

            scope = Scope(name=s)
            db.add(scope)
        db.commit()

    @classmethod
    def random_user_data(cls, quantity: int = 1) -> Union[List[dict], dict]:
        faker = Faker()
        data = [{
            "full_name": faker.name(),
            "email": faker.email(),
            "password": faker.pystr()
        } for _ in range(quantity)]

        return data[0] if len(data) == 1 else data

    @classmethod
    def clear_users(cls, db):
        db.execute("DELETE FROM users_scopes")
        db.execute("DELETE FROM users")
        db.commit()
