
# News Blog Backend - Django REST Framework

Este es el backend de una aplicación de noticias construido con Django y Django REST Framework. El proyecto incluye autenticación basada en JWT y permite la gestión de usuarios y noticias.

## Requisitos

Asegúrate de tener instalado lo siguiente:

- Python 3.8 o superior
- Django 5.1 o superior
- Django REST Framework
- PostgreSQL (opcional, puedes usar SQLite para desarrollo)
- Django CORS Headers
- Django Simple JWT

## Instalación

Sigue los pasos a continuación para levantar el proyecto localmente:

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/news-blog-backend.git
cd news-blog-backend
```

### 2. Crear y activar un entorno virtual

```bash
python -m venv env
source env/bin/activate  # En MacOS/Linux
env\Scripts\activate     # En Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Crea un archivo `.env` en la raíz del proyecto y añade tus configuraciones de entorno:

```
SECRET_KEY=tu_secreto
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3  # Usa PostgreSQL en producción
```

### 5. Realizar migraciones

```bash
python manage.py migrate
```

### 6. Crear un superusuario

```bash
python manage.py createsuperuser
```

### 7. Levantar el servidor de desarrollo

```bash
python manage.py runserver
```

Ahora puedes acceder a la API en `http://localhost:8000`.

## Endpoints

### Autenticación JWT

- **Obtener token de acceso y refresh**:
  - **POST** `http://localhost:8000/api/token/`
    - Parámetros: `{ "username": "<username>", "password": "<password>" }`
    - Respuesta: `{ "access": "<access_token>", "refresh": "<refresh_token>" }`

- **Refrescar token**:
  - **POST** `http://localhost:8000/api/token/refresh/`
    - Parámetros: `{ "refresh": "<refresh_token>" }`
    - Respuesta: `{ "access": "<new_access_token>" }`

### Usuarios

- **Registro de un nuevo usuario**:
  - **POST** `http://localhost:8000/api/register/`
    - Parámetros: `{ "username": "<username>", "email": "<email>", "password": "<password>" }`
    - Respuesta: Detalles del nuevo usuario registrado.

- **Obtener perfil del usuario autenticado**:
  - **GET** `http://localhost:8000/api/profile/`
    - Debes enviar el token JWT en el encabezado:
      ```plaintext
      Authorization: Bearer <access_token>
      ```
    - Respuesta: Información del usuario autenticado (`username`, `email`, etc.).

- **Listado de usuarios (solo para admins)**:
  - **GET** `http://localhost:8000/api/users/`
    - Solo accesible para administradores.

- **Eliminar usuario (solo para admins)**:
  - **DELETE** `http://localhost:8000/api/users/<id>/`
    - Solo accesible para administradores.

### Noticias

- **Obtener listado de noticias**:
  - **GET** `http://localhost:8000/api/news/`
    - Respuesta: Listado de noticias, accesible para cualquier usuario.

- **Crear una noticia (solo usuarios autenticados)**:
  - **POST** `http://localhost:8000/api/news/`
    - Debes enviar el token JWT en el encabezado.
    - Parámetros: `{ "title": "<title>", "description": "<description>", "image": "<image>", "video_url": "<optional>" }`
    - Respuesta: Detalles de la noticia creada.

- **Editar una noticia (solo autor o admin)**:
  - **PUT** `http://localhost:8000/api/news/<id>/`
    - Solo accesible para el autor de la noticia o un administrador.

- **Eliminar una noticia (solo autor o admin)**:
  - **DELETE** `http://localhost:8000/api/news/<id>/`
    - Solo accesible para el autor o un administrador.

## Archivos estáticos y medios

Si estás manejando archivos estáticos o de medios, asegúrate de tener configurado el servidor de archivos estáticos correctamente para entornos de producción. Durante el desarrollo, puedes utilizar la configuración por defecto de Django:

```bash
python manage.py collectstatic
```

## .gitignore recomendado

Aquí tienes un archivo **`.gitignore`** recomendado para tu proyecto:

```plaintext
# Entorno de Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.env
*.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Archivos de configuración de Django
db.sqlite3
*.sqlite3
*.log

# Archivos de medios
media/

# Archivos estáticos generados
static/

# Secretos y variables de entorno
.env

# Archivos de VSCode y MacOS
.vscode/
.DS_Store

# Archivos de migraciones de Django
*/migrations/*.pyc
*/migrations/__pycache__/
```

Este archivo `.gitignore` evita que subas archivos generados localmente, configuraciones del entorno de desarrollo, bases de datos SQLite, y otros archivos temporales.

## Contribución

Si deseas contribuir al proyecto, por favor, envía un pull request o abre un issue para discutir el cambio.

## Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).
