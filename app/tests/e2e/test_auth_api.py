from typing import Tuple

import httpx

from app.tests.factories import UserFactory
from app.auth.scopes import LIST_USERS


def register_user(client) -> dict:
    user_data = UserFactory.random_user_data()

    response = client.post(
        "/api/v1/register",
        json=user_data
    )

    assert response.status_code == 200

    return user_data


def login_user(client, credentials: dict) -> httpx.Response:
    return client.post(
        "/api/v1/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": credentials.get("email"), "password": credentials.get("password")}
    )


def test_happy_path_success_login(db, client):
    user_data = register_user(client)

    response = login_user(client, user_data)

    assert response.status_code == 200


def test_unhappy_path_fail_login(db, client):
    user_data = register_user(client)

    response = login_user(
        client,
        {**user_data, "password": user_data["password"] + "aaa"}
    )

    assert response.status_code == 400


def test_happy_path_list_users(db, client):
    UserFactory.clear_users(db)

    register_user(client)
    register_user(client)
    register_user(client)

    UserFactory.create_scopes(db, scopes=[LIST_USERS])
    user, password = UserFactory.sample_user(db, scopes=[LIST_USERS])

    login_response = login_user(client, {"email": user.email, "password": password})

    assert login_response.status_code == 200

    token = login_response.json().get("access_token")
    response = client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json().get("total") == 4
