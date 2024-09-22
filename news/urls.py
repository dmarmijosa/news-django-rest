from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, UserViewSet, UserCreateView, UserProfileView

# Definir el router para el CRUD de noticias y usuarios
router = DefaultRouter()
router.register(r'news', NewsViewSet)
router.register(r'users', UserViewSet, basename='user')  # Registrar el UserViewSet para CRUD de usuarios

# Definir las rutas para la API
urlpatterns = [
    path('', include(router.urls)),  # Incluye las rutas del router
    path('register/', UserCreateView.as_view(), name='user-register'),  # Ruta para el registro de usuarios
    path('profile/', UserProfileView.as_view(), name='user-profile'),  # Ruta de perfil fuera del router
]
