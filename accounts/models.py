from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    picture = models.ImageField(
        default="habits/profile_pics/default.png", upload_to="habits/profile_pics"
    )
