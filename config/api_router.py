from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from django.urls import path

from asistencias.users.api.views import UserViewSet
from core.api import CursoList, AlumnoViewSet, AsistenciaViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("alumnos", AlumnoViewSet)
router.register("asistencia", AsistenciaViewSet)

app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path("cursos/", CursoList.as_view(), name="curso-list"),
]

