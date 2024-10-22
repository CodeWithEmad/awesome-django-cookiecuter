import pytest
from apps.users.models import User
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUserViews:

    def test_user_list_admin_access(self, api_client, user_factory):
        # Create an admin user
        admin = user_factory(is_staff=True)
        api_client.force_authenticate(user=admin)

        # Create some test users
        user_factory.create_batch(3)

        url = reverse("user-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4  # 3 created users + 1 admin

    def test_user_list_normal_user_access(self, api_client, user_factory):
        # Create a normal user
        user = user_factory()
        api_client.force_authenticate(user=user)

        url = reverse("user-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_detail(self, api_client, user_factory):
        user = user_factory()
        api_client.force_authenticate(user=user)

        url = reverse("user-detail", kwargs={"pk": user.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == user.username
        assert response.data["email"] == user.email

    def test_user_create_unauthenticated(self, api_client):
        url = reverse("user-list")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword123",
        }

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username="newuser").exists()
        assert "user" in response.data
        assert "refresh" in response.data
        assert "access" in response.data

    def test_user_create_authenticated(self, api_client, user_factory):
        user = user_factory()
        api_client.force_authenticate(user=user)

        url = reverse("user-list")
        data = {
            "username": "newuser2",
            "email": "newuser2@example.com",
            "password": "securepassword123",
        }

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username="newuser2").exists()

    def test_user_update(self, api_client, user_factory):
        user = user_factory()
        api_client.force_authenticate(user=user)

        url = reverse("user-detail", kwargs={"pk": user.pk})
        data = {"email": "updated@example.com"}

        response = api_client.patch(url, data)

        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.email == "updated@example.com"

    def test_user_delete(self, api_client, user_factory):
        user = user_factory()
        api_client.force_authenticate(user=user)

        url = reverse("user-detail", kwargs={"pk": user.pk})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(pk=user.pk).exists()

    def test_me_endpoint(self, api_client, user_factory):
        user = user_factory()
        api_client.force_authenticate(user=user)

        url = reverse("user-me")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == user.username
        assert response.data["email"] == user.email

    def test_me_endpoint_unauthenticated(self, api_client):
        url = reverse("user-me")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize("is_staff", [True, False])
    def test_user_list_permission(self, api_client, user_factory, is_staff):
        user = user_factory(is_staff=is_staff)
        api_client.force_authenticate(user=user)

        url = reverse("user-list")
        response = api_client.get(url)

        expected_status = status.HTTP_200_OK if is_staff else status.HTTP_403_FORBIDDEN
        assert response.status_code == expected_status

    def test_user_create_with_tokens(self, api_client):
        url = reverse("user-list")
        data = {
            "username": "tokenuser",
            "email": "tokenuser@example.com",
            "password": "securepassword123",
        }

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert "user" in response.data
        assert "refresh" in response.data
        assert "access" in response.data

        # Verify the tokens work
        access_token = response.data["access"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        me_url = reverse("user-me")
        me_response = api_client.get(me_url)

        assert me_response.status_code == status.HTTP_200_OK
        assert me_response.data["username"] == "tokenuser"
