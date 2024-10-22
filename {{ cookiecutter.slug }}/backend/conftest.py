import factory
import pytest
from apps.users.models import User
from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework.test import APIClient

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: fake.user_name())
    email = factory.LazyAttribute(lambda _: fake.email())
    password = factory.PostGenerationMethodCall("set_password", "password123")


@pytest.fixture
def user_factory():
    return UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword123",
    }


@pytest.fixture
def created_user(db, user_data):
    User = get_user_model()
    return User.objects.create_user(**user_data)
