from rest_framework import viewsets, generics, permissions, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth.models import User, Group
from .models import News
from .serializers import NewsSerializer, UserSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permiso personalizado que permite solo a los dueños de las noticias o a los administradores
    editar y eliminar.
    """
    def has_object_permission(self, request, view, obj):
        # Permitir acciones GET, HEAD o OPTIONS para todos
        if request.method in permissions.SAFE_METHODS:
            return True
        # Solo los administradores o los autores de la noticia pueden modificarla
        return obj.author == request.user or request.user.is_staff

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]

    def get_queryset(self):
        # Si el usuario es admin, puede ver todas las noticias, si no, cualquiera puede verlas
        if self.request.user.is_staff:
            return News.objects.all()
        return News.objects.all()  # Cualquier usuario puede ver todas las noticias

    def perform_create(self, serializer):
        # Asignar el autor como el usuario autenticado
        serializer.save(author=self.request.user)

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Guardar el usuario
        user = serializer.save()
        
        # Asegurar que el grupo 'Publicador' existe o crearlo si es necesario
        publicador_group, created = Group.objects.get_or_create(name='Publicador')
        
        # Añadir al grupo usando add(), no asignar directamente
        user.groups.add(publicador_group)

class UserViewSet(viewsets.ModelViewSet):  # Cambiado a ModelViewSet para habilitar CRUD
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    def destroy(self, request, *args, **kwargs):
        # Evitar que el admin se autoelimine
        user = self.get_object()
        if request.user == user:
            raise ValidationError({"detail": "No puedes eliminar tu propio usuario."})

        # Proceder con la eliminación si no es el propio usuario
        self.perform_destroy(user)
        return Response({"message": "delete"}, status=status.HTTP_200_OK)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'groups': [group.name for group in user.groups.all()]  # Obtener los nombres de los grupos
        })