# Prueba Técnica - Sistema de Login y Visualización de Datos

Este proyecto implementa un sistema de autenticación y tabla de datos con reglas de visibilidad según rol. Está basado en **Litestar** para el backend y utiliza HTML/CSS/JavaScript en el frontend.

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
- `venv` (o cualquier entorno virtual de Python)
- pip para instalar dependencias

> En Windows se recomienda ejecutar desde un PowerShell con permisos adecuados.

## 🚀 Instalación y puesta en marcha

1. **Clonar el repositorio**

   ```powershell
   git clone <repo-url> Prueba-Tecnica-Clerc-Carvajal
   cd Prueba-Tecnica-Clerc-Carvajal\backend\appLitestar
   ```

2. **Crear un entorno virtual y activarlo**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Instalar dependencias**

   ```powershell
   pip install -r requirements.txt
   # (si no existe este archivo, ver sección "Dependencias" abajo)
   ```

4. **Configurar / inicializar base de datos**

   - Por defecto intenta conectarse a MySQL si las variables de entorno (p.ej. `DATABASE_URL`) apuntan a un servidor.
   - Fallback automático a SQLite (`test.db`) cuando no hay conexión MySQL.

   Para cargar los datos de `datosBrutos.json`:

   ```powershell
   python subirDatosABaseDatos.py
   ```

   Esto creará las tablas y añadirá usuarios con contraseña `12345` (hash).

5. **Iniciar la aplicación**

   ```powershell
   cd .\backend\appLitestar\ // para acceder a la carpeta con el app.py
   python app.py
   ```

   Por defecto se sirve en `http://localhost:8000` (ver salida del servidor litestar).

6. **Abrir en el navegador**

   Navegar a `http://localhost:8000/auth/login-page` para ver la pantalla de login.


## 🔐 Usuarios de ejemplo

Los usuarios iniciales se cargan desde `data/datosBrutos.json`. El archivo no incluye contraseñas: el script `subirDatosABaseDatos.py` genera usuarios con contraseña genérica `12345` (hasheada). Puedes modificar esto o insertar nuevos usuarios directamente en la base.

Roles disponibles: `admin`, `supervisor`, `usuario`.

## 🧩 Flujo de la aplicación

1. El cliente envía POST a `/auth/login` con JSON `{username, password}`.
2. El servidor verifica credenciales, crea sesión y responde con `nombre` y `rol`.
3. El frontend muestra la tabla y llama a `/auth/data`.
4. El servidor filtra datos según el rol y devuelve un arreglo de registros.
5. Logout mediante POST a `/auth/logout` que borra la sesión.

## ✅ Cumplimiento de requisitos

- Autenticación con contraseña hasheada (`bcrypt`).
- Gestión de sesiones server-side.
- Filtrado de datos según rol.
- Frontend sencillo con DataTables y jQuery.
- Sistema de persistencia con SQLAlchemy y script de carga.


## 📦 Dependencias

Algunas dependencias usadas:

- `litestar`
- `sqlalchemy`
- `aiomysql` / `aiosqlite`
- `passlib`
- `Jinja2` (a través de `litestar.contrib.jinja`)

