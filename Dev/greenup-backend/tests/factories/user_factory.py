# tests/factories/user_factory.py
import factory

from app.db.models.user import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.Faker("email")
    hashed_password = "hashed"
    is_active = True
