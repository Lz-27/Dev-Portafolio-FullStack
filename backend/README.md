# 🐍 Backend API — Portafolio Profesional

API RESTful robusta y asíncrona desarrollada con **FastAPI**, **SQLAlchemy ORM** y **Pydantic v2**. Diseñada para alimentar el portafolio profesional, manejar autenticación administrativa basada en tokens JWT, persistir proyectos y certificaciones, y gestionar el procesamiento de mensajes de contacto con notificaciones vía email en segundo plano.

---

## 🏗️ Arquitectura y Tecnologías

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (v0.115+)
- **Servidor ASGI**: [Uvicorn](https://www.uvicorn.org/) (Standard)
- **Validación y Configuración**: [Pydantic v2](https://docs.pydantic.dev/) + `pydantic-settings`
- **ORM / Base de Datos**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/) con soporte para SQLite (desarrollo) y PostgreSQL (producción)
- **Seguridad**: OAuth2 Password Bearer Flow, JWT (`python-jose[cryptography]`), hashing de contraseñas con `bcrypt`
- **Email Asíncrono**: `aiosmtplib` ejecutado en `BackgroundTasks` de FastAPI
- **Rate Limiting**: `slowapi` integrado para protección contra spam en endpoints públicos

---

## 📁 Estructura del Proyecto

```text
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py            # Login OAuth2/JSON, Refresh Token, /auth/me
│   │       │   ├── certifications.py  # CRUD y listado público de certificaciones
│   │       │   ├── messages.py        # Envío de contacto + bandeja de entrada admin
│   │       │   └── projects.py        # CRUD y listado público de proyectos con filtros
│   │       └── router.py              # Agregador unificado de routers v1
│   ├── core/
│   │   ├── config.py                  # Settings validados vía Pydantic BaseSettings
│   │   ├── dependencies.py            # Inyección de dependencias (DB Session, Auth Admin/User)
│   │   └── security.py                # Hashing bcrypt y generación/validación JWT
│   ├── crud/
│   │   ├── crud_certification.py      # Operaciones DB para Certificaciones
│   │   ├── crud_message.py            # Operaciones DB para Mensajes
│   │   ├── crud_project.py            # Operaciones DB para Proyectos
│   │   └── crud_user.py               # Autenticación y gestión de Usuarios
│   ├── db/
│   │   ├── database.py                # Engine SQLAlchemy y SessionLocal
│   │   └── init_db.py                 # Lifespan hook: migración de tablas y auto-seed
│   ├── models/                        # Entidades declarativas SQLAlchemy (User, Project, etc.)
│   ├── schemas/                       # DTOs y validadores Pydantic (Request/Response)
│   └── utils/                         # Utilitarios (auditoría IP, cliente SMTP)
├── .env.example                       # Plantilla de variables de entorno
├── main.py                            # Entrypoint ASGI, middlewares (CORS, handlers) y lifespan
├── portafolio.db                      # Base de datos SQLite local
├── postman_collection.json            # Colección de pruebas de Postman
└── requirements.txt                   # Dependencias fijadas de Python
```

---

## ⚙️ Variables de Entorno (`.env`)

Copia el archivo de ejemplo para configurar tu entorno local:

```bash
cp .env.example .env
```

| Variable | Tipo | Descripción | Por Defecto |
| :--- | :--- | :--- | :--- |
| `APP_NAME` | `str` | Nombre de la aplicación | `"Portafolio API"` |
| `APP_VERSION` | `str` | Versión del API | `"1.0.0"` |
| `DEBUG` | `bool` | Modo depuración (expone trazas detalladas) | `True` |
| `ENVIRONMENT` | `str` | Entorno de ejecución (`development`, `production`) | `"development"` |
| `SECRET_KEY` | `str` | Clave criptográfica para firma de JWT | Requerido |
| `ALGORITHM` | `str` | Algoritmo de cifrado para tokens | `"HS256"` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `int` | Tiempo de vida del access token | `15` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `int` | Tiempo de vida del refresh token | `7` |
| `DATABASE_URL` | `str` | Cadena de conexión SQLAlchemy | `sqlite:///./portafolio.db` |
| `CORS_ORIGINS` | `list` / `json` | Orígenes permitidos por CORS | `["http://localhost:5173"]` |
| `SMTP_HOST` | `str` | Servidor SMTP para envío de emails | `"smtp.gmail.com"` |
| `SMTP_PORT` | `int` | Puerto SMTP TLS | `587` |
| `SMTP_USER` | `str` | Usuario o correo de autenticación SMTP | `""` |
| `SMTP_PASSWORD` | `str` | Contraseña de aplicación SMTP | `""` |
| `FIRST_ADMIN_USERNAME` | `str` | Nombre de usuario inicial para el seed | `"admin"` |
| `FIRST_ADMIN_PASSWORD` | `str` | Contraseña inicial para el seed | `"Admin123!"` |

---

## 🚀 Instalación y Puesta en Marcha

### 1. Entorno Virtual Python
Se recomienda Python 3.10 o superior:

```bash
# Crear entorno virtual
python -m venv venv

# Activar en Windows PowerShell:
.\venv\Scripts\Activate.ps1
# O en Linux/macOS:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar Servidor de Desarrollo

```bash
uvicorn main:app --reload --port 8000
```

Al levantar por primera vez, el hook de **lifespan** ejecutará `init_db`:
1. Crea automáticamente las tablas si no existen.
2. Siembra el usuario administrador por defecto configurado en las variables de entorno.
3. Precarga los proyectos y certificaciones iniciales si las tablas se encuentran vacías.

---

## 📡 Catálogo de Endpoints Principales

Ruta base: `/api/v1`

### 1. Autenticación (`/auth`)
- `POST /auth/login`: Login mediante estándar OAuth2 Password Request Form (utilizado por Swagger UI).
- `POST /auth/login/json`: Login mediante cuerpo JSON (`{"username": "...", "password": "..."}`).
- `POST /auth/token/refresh`: Renueva un token de acceso utilizando un token de refresco válido.
- `GET /auth/me`: Retorna los datos del usuario autenticado (requiere `Authorization: Bearer <token>`).

### 2. Proyectos (`/projects`)
- `GET /projects/`: Listado público paginado (`skip`, `limit`) con filtrado por `categoria` (`frontend`, `fullstack`, `data`, `desktop`, `backend`).
- `GET /projects/{id}`: Consulta un proyecto específico por ID numérico.
- `GET /projects/slug/{slug}`: Consulta un proyecto mediante su slug amigable.
- `POST /projects/`: Creación de proyectos *(Requiere rol Administrador)*.
- `PUT /projects/{id}`: Actualización completa o parcial *(Requiere rol Administrador)*.
- `DELETE /projects/{id}`: Eliminación lógica o soft delete *(Requiere rol Administrador)*.

### 3. Certificaciones (`/certifications`)
- `GET /certifications/`: Listado público paginado con filtros por categoría (`data`, `cloud`, `dev`, etc.).
- `GET /certifications/{id}`: Consulta de detalle por ID.
- `POST /certifications/`: Creación de certificación *(Requiere rol Administrador)*.
- `PUT /certifications/{id}`: Actualización *(Requiere rol Administrador)*.
- `DELETE /certifications/{id}`: Baja lógica *(Requiere rol Administrador)*.

### 4. Mensajes y Contacto (`/messages`)
- `POST /messages/`: Recepción pública de mensajes del formulario web. Valida formato de email, aplica límite de tasa por IP, persiste en base de datos y despacha notificación SMTP asíncrona mediante `BackgroundTasks`.
- `GET /messages/`: Listado de mensajes recibidos *(Requiere rol Administrador)*.
- `GET /messages/{id}`: Detalle de mensaje *(Requiere rol Administrador)*.
- `PUT /messages/{id}/read`: Marca de estado leído/no leído *(Requiere rol Administrador)*.
- `DELETE /messages/{id}`: Eliminación de mensaje *(Requiere rol Administrador)*.

### 5. Diagnóstico
- `GET /api/v1/health`: Estado operacional del servicio y entorno activo.

---

## 📖 Documentación Interactiva

FastAPI genera documentación OpenAPI de manera automática:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Colección Postman**: Importa el archivo [postman_collection.json](file:///c:/PROYECTOS/FRONTEND/2.%20Portafolio%20V2/backend/postman_collection.json) para ejecutar peticiones preconfiguradas.
