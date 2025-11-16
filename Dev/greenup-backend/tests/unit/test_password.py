# tests/unit/test_password.py
from app.core.security.password import get_password_service


def test_hash_and_verify():
    pwd = get_password_service()
    hashed = pwd.hash("secret")
    assert pwd.verify(hashed, "secret") is True
    assert pwd.verify(hashed, "wrong") is False
