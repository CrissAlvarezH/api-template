import pytest

from app.auth.utils import get_password_hash, verify_password


@pytest.mark.parametrize(
    "password",
    ["12345", "abcd123", "helloword", "Adfdh!@af.ad,!@f.a-,"]
)
def test_hash_password(password):
    password_hash = get_password_hash(password)

    assert password != password_hash
    is_password_valid = verify_password(password, password_hash)

    assert is_password_valid

