# Prueba Técnica - Sistema de Login y Visualización de Datos

Este proyecto implementa un sistema de autenticación y tabla de datos con reglas de visibilidad según rol. Está basado en **Litestar** para el backend y utiliza HTML/CSS/JavaScript en el frontend.

## 🚀 Despliegue en Render

El proyecto está disponible en **Render**. Puedes acceder en el siguiente enlace (nota: la aplicación puede estar durmiendo al principio, espera aproximadamente 1 minuto para que se termine de desplegar):

```
https://prueba-tecnica-clerc-carvajal.onrender.com/auth/login-page
```

### Credenciales de ejemplo

| Rol | Usuario | Contraseña |
|------|---------|-----------|
| **Administrador** | `jhon_doe` | `12345` |
| **Supervisor** | `ana_torres` | `12345` |
| **Usuario** | `camila_navarro` | `12345` |


## 📁 Estructura principal

```
backend/
  appLitestar/
    app.py              # punto de entrada de la aplicación
    data/datosBrutos.json  # usuarios de ejemplo
    subirDatosABaseDatos.py # script para poblar la base de datos
    controller/         # controladores (rutas)
    services/           # lógica de negocio y autenticación
    repositories/       # acceso a base de datos
    database/           # modelos y sesión SQLAlchemy
    static/             # archivos estáticos (JS, CSS)
    templates/          # vistas HTML (Jinja)
```

## 🛠 Requisitos previos

- Python 3.10+ (recomendado 3.11)
- `venv` o cualquier gestor de entornos virtuales de Python
- pip para instalar dependencias

> **Nota:** Se recomienda usar Windows PowerShell o Visual Studio Code para ejecutar los comandos.

## 🚀 Instalación y Configuración

### Paso 1: Clonar el repositorio

```powershell
git clone https://github.com/BastianRivas/Prueba-Tecnica-Clerc-Carvajal
cd Prueba-Tecnica-Clerc-Carvajal
```

### Paso 2: Acceder a la carpeta del backend

```powershell
cd backend\appLitestar
```

### Paso 3: Crear y activar entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Paso 4: Instalar dependencias

```powershell
pip install -r requirements.txt
```

### Paso 5: Configurar la base de datos (opcional)

Por defecto, la aplicación usa **SQLite (`test.db`)** como fallback automático.

Si deseas usar **MySQL**, configura una variable de entorno:

```powershell
$env:DATABASE_URL = "mysql+aiomysql://usuario:password@localhost:3306/nombre_db"
```

### Paso 6: Cargar datos iniciales (Primera ejecución)

```powershell
python subirDatosABaseDatos.py
```

Este script crea las tablas y añade usuarios con contraseña `12345` (hasheada con bcrypt).

### Paso 7: Iniciar la aplicación

```powershell
uvicorn app:app --reload
```

La aplicación estará disponible en: `http://localhost:8000/auth/login-page`


## 🔐 Usuarios de ejemplo

Los usuarios iniciales se cargan desde `data/datosBrutos.json`. El script `subirDatosABaseDatos.py` crea usuarios con contraseña genérica `12345` (hasheada con bcrypt). 

**Roles disponibles:**
- `admin` - Acceso total a todos los datos
- `supervisor` - Acceso a supervisores y usuarios
- `usuario` - Acceso solo a sus propios datos

## 🧩 Flujo de la aplicación

1. El cliente envía `POST /auth/login` con JSON `{username, password}`.
2. El servidor verifica credenciales contra la base de datos.
3. Si son válidas, se crea una sesión en el servidor y se devuelve `nombre` y `rol`.
4. El frontend muestra el dashboard y llama a `GET /auth/data`.
5. El servidor filtra los datos según el rol del usuario y devuelve el arreglo de registros.
6. Los datos se cargan en una tabla DataTables para visualización interactiva.
7. El logout mediante `POST /auth/logout` borra la sesión en el servidor.

## ✅ Características implementadas

### Funcionalidad
- ✅ Sistema de login con autenticación basada en usuario y contraseña
- ✅ Gestión de sesiones server-side con Litestar
- ✅ Tres roles de usuario: `admin`, `supervisor`, `usuario`
- ✅ Visualización de datos filtrados según rol
- ✅ Tabla interactiva con DataTables y jQuery
- ✅ Logout funcional

### Seguridad
- ✅ Contraseñas hasheadas con bcrypt (máximo 72 caracteres)
- ✅ Validación de credenciales en el backend
- ✅ Sesiones almacenadas en el servidor (no en cookies)

### Extras implementados
- ✅ Uso de **DataTables** para visualización de datos
- ✅ Implementación de **hashing de contraseñas** con passlib/bcrypt
- ✅ **Base de datos** con SQLAlchemy (SQLite/MySQL)
- ✅ Script de **seed de datos** (`subirDatosABaseDatos.py`)
- ✅ **Despliegue en producción** (Render)
- ✅ Código bien estructurado con Controllers, Services y Repositories


## 📦 Dependencias

| Paquete | Descripción |
|---------|-----------|
| `litestar` | Framework web asíncrono moderno |
| `sqlalchemy` | ORM y herramientas de base de datos |
| `aiomysql` | Soporte asíncrono para MySQL |
| `aiosqlite` | Soporte asíncrono para SQLite |
| `passlib` | Biblioteca de hashing de contraseñas |
| `bcrypt` | Algoritmo de hashing de contraseñas |
| `Jinja2` | Motor de plantillas (vía `litestar.contrib.jinja`) |
| `uvicorn` | Servidor ASGI de alto rendimiento |


## 📝 Notas

- El archivo `requirements.txt` debe estar en la carpeta `backend/appLitestar/`
- El proyecto usa variables de entorno para configuración (p.ej., `DATABASE_URL`)
- La sesión se mantiene mediante un ID almacenado en cookies y datos en el servidor

