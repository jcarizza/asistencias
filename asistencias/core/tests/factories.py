from collections.abc import Sequence
from typing import Any

from factory import Faker
from factory.fuzzy import FuzzyInteger
from factory import post_generation
from factory.django import DjangoModelFactory
from rest_framework.authtoken.models import Token

from asistencias.users.models import User
from asistencias.core.models import Preceptor, Docente, Alumno


class UserFactory(DjangoModelFactory):
    username = FuzzyInteger(10000000, 50000000)
    email = Faker("email")
    name = Faker("name")

    class Meta:
        model = User
        django_get_or_create = ["username"]


class PreceptorFactory(DjangoModelFactory):
    user = UserFactory()

    class Meta:
        model = Preceptor


class DocenteFactory(DjangoModelFactory):
    user = UserFactory()

    class Meta:
        model = Docente


class AlumnoFactory(DjangoModelFactory):
    user = UserFactory()

    class Meta:
        model = Alumno
