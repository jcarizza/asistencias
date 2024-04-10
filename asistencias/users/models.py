from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from rest_framework.authtoken.models import Token


class User(AbstractUser):

    # First and last name do not cover name patterns around the globe
    username = CharField(_("Username"), max_length=8, unique=True)
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    USERNAME_FIELD = "username"

    def __str__(self):
        return str(self.username)

    def get_absolute_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.username})

    def is_preceptor(self):
        return hasattr(self, "preceptor")

    def is_docente(self):
        return hasattr(self, "docente")

    def is_alumno(self):
        return hasattr(self, "alumno")

    @property
    def token(self):
        t, _ = Token.objects.get_or_create(user=self)
        return t
