import pytest
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError


@pytest.mark.django_db
def test_create_user(user_data):
    User = get_user_model()
    user = User.objects.create_user(**user_data)
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]
    assert user.check_password(user_data["password"])


@pytest.mark.django_db
def test_create_superuser(user_data):
    User = get_user_model()
    user = User.objects.create_superuser(**user_data)
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]
    assert user.check_password(user_data["password"])
    assert user.is_staff
    assert user.is_superuser


@pytest.mark.django_db
def test_user_str_method(created_user):
    assert str(created_user) == created_user.username


@pytest.mark.django_db
def test_user_email_unique(user_data):
    User = get_user_model()
    User.objects.create_user(**user_data)
    with pytest.raises(IntegrityError):
        User.objects.create_user(**user_data)


@pytest.mark.django_db
def test_user_username_unique(user_data):
    User = get_user_model()
    User.objects.create_user(**user_data)
    with pytest.raises(IntegrityError):
        User.objects.create_user(**user_data)


@pytest.mark.django_db
def test_user_set_password(user_data):
    User = get_user_model()
    user = User.objects.create_user(**user_data)
    user.set_password("newpassword123")
    assert user.check_password("newpassword123")


@pytest.mark.django_db
def test_user_has_perm(created_user):
    assert not created_user.has_perm("users.view_user")
    assert not created_user.has_perm("users.change_user")
    assert not created_user.has_perm("users.add_user")
    assert not created_user.has_perm("users.delete_user")


@pytest.mark.django_db
def test_user_get_full_name(created_user):
    full_name = f"{created_user.first_name} {created_user.last_name}"
    assert created_user.get_full_name() == full_name.strip()


@pytest.mark.django_db
def test_user_get_short_name(created_user):
    assert created_user.get_short_name() == created_user.first_name


@pytest.mark.django_db
def test_user_email_normalization(user_data):
    User = get_user_model()
    email = "testuser@EXAMPLE.COM"
    user_data["email"] = email
    user = User.objects.create_user(**user_data)
    assert user.email == email.lower()


@pytest.mark.django_db
def test_user_is_active_by_default(user_data):
    User = get_user_model()
    user = User.objects.create_user(**user_data)
    assert user.is_active


@pytest.mark.django_db
def test_superuser_has_all_permissions(user_data):
    User = get_user_model()
    user = User.objects.create_superuser(**user_data)
    assert user.has_perm("users.view_user")
    assert user.has_perm("users.change_user")
    assert user.has_perm("users.add_user")
    assert user.has_perm("users.delete_user")
