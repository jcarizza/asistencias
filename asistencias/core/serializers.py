from rest_framework import serializers
from asistencias.core.models import Alumno, Asistencia, Curso


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = "__all__"  # Incluye todos los campos del modelo Curso


class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = "__all__"


class AsistenciaSerializer(serializers.ModelSerializer):
    alumnos = AlumnoSerializer(many=True, source="lista_alumnos")

    class Meta:
        model = Asistencia
        fields = "__all__"
