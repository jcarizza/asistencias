from datetime import datetime

from factory import Faker
from factory.fuzzy import FuzzyInteger, FuzzyDate
from factory.django import DjangoModelFactory

from asistencias.users.models import User
from asistencias.core.models import (
    PoapAsistencia,
    Asistencia,
    Preceptor,
    Docente,
    Alumno,
    Curso,
)


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


class CursoFactory(DjangoModelFactory):
    class Meta:
        model = Curso


class AsistenciaFactory(DjangoModelFactory):
    fecha = FuzzyDate(datetime.now().date())
    curso = CursoFactory()

    class Meta:
        model = Asistencia


class PoapAsistenciaFactory(DjangoModelFactory):
    alumno = AlumnoFactory()

    class Meta:
        model = PoapAsistencia
