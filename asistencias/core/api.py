from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Alumno, Curso, Asistencia
from .serializers import (
    AlumnoSerializer,
    AsistenciaSerializer,
    CursoSerializer,
    TomarAsistenciaSerializer,
)
from .permissions import IsOwnerAlumno, IsPreceptor, IsDocente
from asistencias.core.services import ClimaService


class CursoList(generics.ListAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
    permission_classes = [IsAuthenticated, IsOwnerAlumno | IsPreceptor]


class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer
    permission_classes = [IsAuthenticated, IsPreceptor | IsDocente]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return TomarAsistenciaSerializer
        return self.serializer_class


class Clima(APIView):

    def get(self, request, format=None):
        return Response({
            "clima": ClimaService.get_clima()
        })
