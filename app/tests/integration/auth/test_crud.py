from app.auth import crud
from app.auth.schemas import UserCreate, UserUpdate

from app.tests.factories import UserFactory


def test_create_and_get_users(db):
    user_data = UserFactory.random_user_data()

    # test create user
    user_created = crud.create_user(db, UserCreate(**user_data))

    assert user_created.full_name == user_data.get("full_name")
    assert user_created.email == user_data.get("email")

    # test get user
    user_in_db = crud.get_user_by_email(db, user_data.get("email"))

    assert user_in_db.full_name == user_data.get("full_name")

    user_in_db = crud.get_user_by_id(db, user_created.id)

    assert user_in_db.full_name == user_created.full_name
    assert user_in_db.email == user_created.email

    db.delete(user_in_db)
    db.commit()


def test_list_users(db):
    quantity_user = 12
    users_data = UserFactory.random_user_data(quantity_user)

    for user_data in users_data:
        crud.create_user(db, UserCreate(**user_data))

    users_in_db = crud.list_users(db)

    assert len(users_in_db) == len(users_data)

    for user in users_in_db:
        db.delete(user)
    db.commit()


def test_update_user(db):
    user, _ = UserFactory.sample_user(db)

    name_changed = user.full_name + "__updated"
    crud.update_user(
        db, user.id, UserUpdate(full_name=name_changed)
    )

    user_updated = crud.get_user_by_id(db, user.id)

    assert user_updated.id == user.id
    assert user_updated.full_name == name_changed

    db.delete(user)
    db.commit()
