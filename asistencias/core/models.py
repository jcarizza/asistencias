from django.db import models


class PersonaManager(models.Manager):
    pass

class AlumnoManager(models.Manager):
    pass

class PreceptorManager(models.Manager):
    pass


class CursoManager(models.Manager):
    pass

class Curso(models.Model):
    nombre = models.CharField(max_length=10, null=True)


    def __str__(self):
        return self.nombre

class Alumno(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)
    curso = models.ForeignKey("Curso", null=True, on_delete=models.CASCADE)

    objects = PersonaManager()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        permissions = [
            ("deshabilitar_alumno", "Deshabilitar alumno"),
        ]

class Preceptor(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)

class Docente(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)


class MotivoAusencia(models.Model):
    text = models.CharField(max_length=30)


class Asistencia(models.Model):
    fecha = models.DateField(null=True)
    curso = models.ForeignKey("Curso", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["fecha", "curso"]
        permissions = [
            ("tomar_asistencia", "Puede tomar asistencia"),
        ]

class PoapAsistencia(models.Model):
    alumno = models.ForeignKey("Alumno", null=True, on_delete=models.CASCADE)
    presente = models.BooleanField(null=True)
    motivo_ausencia = models.ForeignKey("MotivoAusencia", blank=True, null=True, on_delete=models.CASCADE)
    tabla_asistencia = models.ForeignKey("Asistencia", null=True, related_name="lista_alumnos", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["alumno", "tabla_asistencia"]
