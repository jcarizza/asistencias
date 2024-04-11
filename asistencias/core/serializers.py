from rest_framework import serializers
from asistencias.core.models import Alumno, Asistencia, Curso, PoapAsistencia


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = "__all__"  # Incluye todos los campos del modelo Curso


class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = "__all__"


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
        lista = self.validated_data.pop("lista_alumnos")
        tabla_asistencia = Asistencia.objects.create(**self.validated_data)
        for alumno in lista:
            PoapAsistencia.objects.create(**alumno, tabla_asistencia=tabla_asistencia)
        return tabla_asistencia

    class Meta:
        model = Asistencia
        fields = "__all__"
        validators = []
