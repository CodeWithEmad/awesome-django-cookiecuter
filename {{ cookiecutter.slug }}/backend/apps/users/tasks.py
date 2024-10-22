from apps.users.models import User
from celery import shared_task


@shared_task
def get_users_count():
    return User.objects.count()
