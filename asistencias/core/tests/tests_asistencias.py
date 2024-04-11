from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from asistencias.users.tests.factories import UserFactory
from asistencias.core.tests.factories import (
    AlumnoFactory,
    CursoFactory,
    PreceptorFactory,
    PoapAsistenciaFactory,
    AsistenciaFactory,
    DocenteFactory,
)


class AsistenciasViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.preceptor = PreceptorFactory.create()
        self.preceptor.user.save()
        self.docente = DocenteFactory.create()
        self.docente.user.save()
        self.alumno = AlumnoFactory.create()
        self.alumno.user.save()

        self.curso = CursoFactory.create()
        self.asistencia = AsistenciaFactory.create(curso=self.curso)
        for n in range(0, 10):
            user = UserFactory.create()
            alumno = AlumnoFactory.create(curso=self.curso, user=user)
            PoapAsistenciaFactory.create(
                alumno=alumno,
                tabla_asistencia=self.asistencia,
                presente=True,
            )

    def test_preceptor_puede_listar_asistencias(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.preceptor.user.token.key
        )
        response = self.client.get("/api/asistencias/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_preceptor_puede_ver_asistencia(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.preceptor.user.token.key
        )
        response = self.client.get(f"/api/asistencias/{self.asistencia.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_docente_puede_listar_asistencias(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.docente.user.token.key
        )
        response = self.client.get("/api/asistencias/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_docente_puede_ver_asistencia(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.docente.user.token.key
        )
        response = self.client.get(f"/api/asistencias/{self.asistencia.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_alumno_no_puede_listar_asistencias(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.alumno.user.token.key
        )
        response = self.client.get("/api/asistencias/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_alumno_no_puede_ver_asistencia(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.alumno.user.token.key
        )
        response = self.client.get(f"/api/asistencias/{self.asistencia.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_preceptor_toma_asistencia(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.preceptor.user.token.key
        )
        data = {
            "fecha": "2024-04-24",
            "curso": self.curso.id,
            "lista_alumnos": [
                {
                    "alumno": self.alumno.id,
                    "presente": True,
                    "motivo_ausencia": None,
                }
            ],
        }
        response = self.client.post("/api/asistencias/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
