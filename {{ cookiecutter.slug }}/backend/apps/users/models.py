from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom user model that extends the default Django AbstractUser model.

    This model can be used to add additional fields or methods specific
    to your application's user requirements while retaining the default
    Django User functionalities.
    """

    email = models.EmailField(_("Email"), max_length=254, unique=True)
    username = models.CharField(
        _("Username"),
        max_length=50,
        unique=True,
        help_text=_(
            "Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[
            AbstractUser.username_validator,
            MinLengthValidator(
                3,
                _("Username must be at least 3 characters long."),
            ),
        ],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
