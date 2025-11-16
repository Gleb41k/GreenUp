# tests/unit/test_jwt.py
from datetime import timedelta

from app.core.security.jwt import create_access_token, verify_token


def test_create_and_verify_token():
    token = create_access_token({"sub": "1"}, timedelta(minutes=1))
    payload = verify_token(token)
    assert payload["sub"] == "1"
    assert "exp" in payload
