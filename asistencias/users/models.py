from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    # First and last name do not cover name patterns around the globe
    username = CharField(_("Username"), max_length=8, unique=True)
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    USERNAME_FIELD = "username"

    def get_absolute_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.username})
