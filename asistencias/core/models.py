from django.db import models



class PersonaManager(models.Manager):
    pass

class AlumnoManager(models.Manager):
    pass

class PreceptorManager(models.Manager):
    pass

# Alumno
# user = uno a uno
# permisso:
# - Ver y modificar sus datos
# - Ver sus asistencias
# permissions: deshabilitar_alumno

class CursoManager(models.Manager):
    pass


class Curso(models.Model):
    nombre = models.CharField(max_length=10)

class Alumno(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)
    curso = models.ForeignKey("Curso", on_delete=models.CASCADE)

    objects = PersonaManager()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        permissions = [
            ("deshabilitar_alumno", "Deshabilitar alumno")
        ]


# Preceptor
# user = uno a uno
# - Agregar, deshabilitar, modificar, ver y modificar datos de alumnos
class Preceptor(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)

# Docente
# user = uno a uno
class Docente(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)


class MotivoAusencia(models.Model):
    text = models.CharField(max_length=30)

class TablaAsistencia(models.Model):
    fecha = models.DateField(unique=True)

# Asistencia
# permissions: puede_tomar_asistencia, borrar_asistencia
class PoapAsistencia(models.Model):
    alumno = models.ForeignKey("Alumno", null=True, on_delete=models.CASCADE)
    presente = models.BooleanField(null=True)
    motivo_ausencia = models.ForeignKey("MotivoAusencia", null=True, on_delete=models.CASCADE)
    tabla_asistencia = models.ForeignKey("TablaAsistencia", related_name="lista_alumnos", on_delete=models.CASCADE)
