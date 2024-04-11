import uuid
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from asistencias.users.tests.factories import UserFactory
from asistencias.core.tests.factories import (
    PreceptorFactory,
    AlumnoFactory,
    DocenteFactory,
)
from asistencias.core.models import Alumno


class AlumnoViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = UserFactory.create()
        self.alumno = Alumno.objects.create(user=user, nombre="Juan", apellido="Perez")
        self.alumno_token = Token.objects.create(
            user=user
        )  # Create a token for the test user
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.alumno_token.key
        )  # Include the token in the client's requests

    def _get_client_for_user(self, user):
        t, _ = Token.objects.get_or_create(
            user=user
        )  # Create a token for the test user
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + t.key
        )  # Include the token in the client's requests

    def test_list_alumnos(self):
        response = self.client.get("/api/alumnos/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_alumno(self):
        response = self.client.get(f"/api/alumnos/{self.alumno.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nombre"], "Juan")
        self.assertEqual(response.data["apellido"], "Perez")

    def test_update_alumno(self):
        data = {"nombre": "Pedro", "apellido": "Gomez"}
        response = self.client.patch(f"/api/alumnos/{self.alumno.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.alumno.refresh_from_db()
        self.assertEqual(self.alumno.nombre, "Pedro")
        self.assertEqual(self.alumno.apellido, "Gomez")

        self.alumno.delete()

    def test_alumno_solo_puede_ver_sus_propios_datos(self):
        # Nuevo usuario
        user = UserFactory.create()
        self.otro_alumno = Alumno.objects.create(
            user=user, nombre="Juan", apellido="Perez"
        )

        response = self.client.get(f"/api/alumnos/{self.alumno.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f"/api/alumnos/{self.otro_alumno.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.otro_alumno.delete()

    def test_preceptor_puede_ver_todos_los_alumnos(self):
        data = {"nombre": "Pedro", "apellido": "Gomez"}

        preceptor = PreceptorFactory.create()
        preceptor.user.save()
        otro_alumno = AlumnoFactory.create()
        otro_alumno.user.save()

        self.client.credentials(HTTP_AUTHORIZATION="Token " + preceptor.user.token.key)

        response = self.client.get(f"/api/alumnos/{self.alumno.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f"/api/alumnos/{otro_alumno.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        otro_alumno.delete()
        preceptor.delete()

    def test_preceptor_puede_modificar_todos_los_alumnos(self):
        data = {"nombre": str(uuid.uuid4()), "apellido": str(uuid.uuid4())}
        data_2 = {"nombre": str(uuid.uuid4()), "apellido": str(uuid.uuid4())}

        preceptor = PreceptorFactory.create()
        preceptor.user.save()
        otro_alumno = AlumnoFactory.create()
        otro_alumno.user.save()

        self.client.credentials(HTTP_AUTHORIZATION="Token " + preceptor.user.token.key)

        response = self.client.patch(f"/api/alumnos/{self.alumno.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK), response
        self.assertEqual(response.data["nombre"], data["nombre"])

        response = self.client.patch(f"/api/alumnos/{otro_alumno.id}/", data_2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nombre"], data_2["nombre"])

        otro_alumno.delete()
        preceptor.delete()

    def test_docente_puede_ver_todos_los_alumnos(self):
        data = {"nombre": "Pedro", "apellido": "Gomez"}

        preceptor = PreceptorFactory.create()
        preceptor.user.save()
        otro_alumno = AlumnoFactory.create()
        otro_alumno.user.save()

        self.client.credentials(HTTP_AUTHORIZATION="Token " + preceptor.user.token.key)

        response = self.client.get(f"/api/alumnos/{self.alumno.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f"/api/alumnos/{otro_alumno.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        otro_alumno.delete()
        preceptor.delete()

    def test_docente_no_puede_modificar_todos_los_alumnos(self):
        data = {"nombre": "Pepe", "apellido": "Cibrian"}

        docente = DocenteFactory.create()
        docente.user.save()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + docente.user.token.key)

        response = self.client.patch(f"/api/alumnos/{self.alumno.id}/", data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        docente.delete()
