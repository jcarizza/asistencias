import logging
from rest_framework import serializers
from asistencias.core.models import Alumno, Asistencia, Curso, PoapAsistencia, MotivoAusencia
from asistencias.core.services import ClimaService

logger = logging.getLogger()

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = "__all__"

class CursoSerializer(serializers.ModelSerializer):
    alumnos = AlumnoSerializer(many=True, read_only=True)

    class Meta:
        model = Curso
        fields = "__all__"  # Incluye todos los campos del modelo Curso

class PoapAsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoapAsistencia
        exclude = ("tabla_asistencia",)
        validators = []


class AsistenciaSerializer(serializers.ModelSerializer):
    lista = PoapAsistenciaSerializer(read_only=True, many=True, source="lista_alumnos")
    alumnos = AlumnoSerializer(many=True, source="curso.alumnos")

    class Meta:
        model = Asistencia
        fields = "__all__"


class AsistenciaCrearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = "__all__"


class TomarAsistenciaSerializer(serializers.ModelSerializer):
    fecha = serializers.DateField()
    curso = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all())
    lista_alumnos = PoapAsistenciaSerializer(many=True)

    def create(self, validated_data):
        clima = ClimaService.get_clima()
        lista = self.validated_data.pop("lista_alumnos")
        tabla_asistencia = Asistencia.objects.create(**self.validated_data)
        for alumno in lista:
            presente = alumno.get("presente")

            if clima == "lluvioso" and not presente:
                alumno["motivo_ausencia"] = MotivoAusencia.get_motivo_lluvioso()
                logger.info("El clima esta lluvioso, falta JUSTIFICADA")

            PoapAsistencia.objects.create(**alumno, tabla_asistencia=tabla_asistencia)
        return tabla_asistencia

    class Meta:
        model = Asistencia
        fields = "__all__"
        validators = []
