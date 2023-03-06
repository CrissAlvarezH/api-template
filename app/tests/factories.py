from typing import Tuple, Union, List

from faker import Faker

from app.auth.models import User
from app.auth.utils import get_password_hash


class UserFactory:
    @classmethod
    def sample_user(cls, db) -> Tuple[User, str]:
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

        return user, user_data.get("password")

    @classmethod
    def random_user_data(cls, quantity: int = 1) -> Union[List[dict], dict]:
        faker = Faker()
        data = [{
            "full_name": faker.name(),
            "email": faker.email(),
            "password": faker.pystr()
        } for _ in range(quantity)]

        return data[0] if len(data) == 1 else data
