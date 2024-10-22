from django.db import models


class TimeStamped(models.Model):
    """
    An Abstract class to use for all models that need to have
    created_at and updated_at fields and to be used as a base
    class for other models to inherit from.

    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
