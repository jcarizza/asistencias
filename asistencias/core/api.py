from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Alumno, Curso, Asistencia
from .serializers import AlumnoSerializer, AsistenciaSerializer, CursoSerializer

class CursoList(generics.ListAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
    #permission_classes = [IsAuthenticated]


class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer
    #permission_classes = [IsAuthenticated]
