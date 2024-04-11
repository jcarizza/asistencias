from rest_framework import permissions


class IsOwnerAlumno(permissions.BasePermission):
    """
    Solo puede editar si es el propio usuario
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsPreceptor(permissions.BasePermission):
    """
    Si es preceptor puede leer y editar el recurso alumno
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_preceptor():
            return True
        return False


class IsDocente(permissions.BasePermission):
    """
    Si es docente solo puede leer el recurso Alumno
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_docente():
            return True
        return False
