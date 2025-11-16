from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class PasswordService:
    """
    Утилита для хэширования паролей (Argon2id).
    Не содержит бизнес-логики — только криптография.
    """

    def __init__(self):
        self.ph = PasswordHasher(
            time_cost=3,
            memory_cost=64 * 1024,  # 64 MB
            parallelism=2,
            hash_len=32,
            salt_len=16,
        )

    def hash(self, password: str) -> str:
        return self.ph.hash(password)

    def verify(self, hashed: str, password: str) -> bool:
        try:
            self.ph.verify(hashed, password)
            return True
        except VerifyMismatchError:
            return False

    def needs_rehash(self, hashed: str) -> bool:
        return self.ph.check_needs_rehash(hashed)


# Singleton
_password_service: PasswordService | None = None


def get_password_service() -> PasswordService:
    global _password_service
    if _password_service is None:
        _password_service = PasswordService()
    return _password_service
