from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Permite solo a los administradores crear, editar o eliminar.
    Las solicitudes GET (lectura) están permitidas a todos.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Permite GET, HEAD o OPTIONS requests para todos
        return request.user and request.user.is_staff  # Solo los administradores pueden modificar
