from rest_framework import serializers
from .models import News, Profile
from django.contrib.auth.models import User, Group

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()  # Anidar el perfil
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all(), required=False)  # Manejar grupos

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'profile', 'groups']
        extra_kwargs = {'password': {'write_only': True}}  # Para que la contraseña sea solo de escritura

    def create(self, validated_data):
        # Extraer los datos del perfil y los grupos anidados
        profile_data = validated_data.pop('profile')
        groups_data = validated_data.pop('groups', None)  # Extraer los grupos si existen
        
        # Crear el usuario
        user = User.objects.create(**validated_data)
        # Establecer la contraseña
        user.set_password(validated_data['password'])
        user.save()

        # Crear o actualizar el perfil asociado
        Profile.objects.update_or_create(user=user, defaults=profile_data)

        # Asignar los grupos usando set(), si se proporcionaron
        if groups_data:
            user.groups.set(groups_data)
        else:
            # Si no se proporcionan grupos, asignar el grupo Publicador por defecto
            publicador_group, created = Group.objects.get_or_create(name='Publicador')
            user.groups.add(publicador_group)

        return user


class NewsSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)  # Ahora incluimos la información del autor con imagen

    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'image', 'video_url', 'published_at', 'author']
