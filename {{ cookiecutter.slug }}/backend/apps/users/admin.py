from apps.users.forms import UserAdminChangeForm, UserAdminCreationForm
from apps.users.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserModelAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
