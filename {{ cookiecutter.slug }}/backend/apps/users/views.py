from typing import Any, Dict, List

from apps.users.models import User
from apps.users.serializers import UserRegistrationSerializer, UserSerializer
from django.contrib.auth.models import update_last_login
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(ModelViewSet):
    """
    A viewset for managing user accounts including creating new users and
    listing existing ones. This viewset applies different permissions based on
    the action being performed (i.e., create or list).

    Attributes:
        queryset: The queryset containing all users.
        serializer_class: The default serializer class for the viewset.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self) -> List[Any]:
        """
        Get the list of permissions that this view requires.

        All users are permitted to create an account, but only admin users are
        permitted to list existing users.

        Returns:
            A list of permission classes.
        """
        if self.action == "create":
            self.permission_classes = [AllowAny]
        elif self.action == "list":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get_serializer_class(self) -> type:
        """
        Get the serializer class to be used for the request.

        If the action is 'create', use the UserRegistrationSerializer; otherwise,
        use the default serializer class.

        Returns:
            The serializer class to be used.
        """
        if self.action == "create":
            return UserRegistrationSerializer
        return super().get_serializer_class()

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Create a new user and generate authentication tokens.

        This method handles user creation by validating the request data with the
        appropriate serializer. Upon successful creation, it generates both access
        and refresh tokens and includes them in the response along with the user data.
        It also updates the last login time for the user.

        Args:
            request: The request object containing user data.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            A response containing user data, refresh token, and access token.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate access and refresh tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # Include both user data and tokens in the response
        response_data: Dict[str, Any] = {
            "user": serializer.data,
            "refresh": str(refresh),
            "access": str(access),
        }

        # Update the last login
        update_last_login(None, user)

        headers = self.get_success_headers(serializer.data)
        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(detail=False, methods=["GET"])
    def me(self, request: Request) -> Response:
        """
        Retrieve the current authenticated user's information.

        This method returns the data of the currently authenticated user.

        Args:
            request: The request object containing authentication information.

        Returns:
            A response containing the authenticated user's data.
        """
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
