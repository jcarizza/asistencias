from django.contrib import admin
from .models import Alumno, Docente, Preceptor

@admin.register(Preceptor)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("nombre")
    search_fields = ("nombre")

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ("apellido", "nombre", "curso")
    search_fields = ("apellido", "nombre", "curso")
    list_filter = ("curso",)

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ("apellido", "nombre")
    search_fields = ("apellido", "nombre")

@admin.register(Preceptor)
class PreceptorAdmin(admin.ModelAdmin):
    list_display = ("apellido", "nombre")
    search_fields = ("apellido", "nombre")

