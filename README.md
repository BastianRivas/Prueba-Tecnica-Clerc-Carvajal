# Sistema de Gestión de Usuarios y Datos (Fullstack)

Este repositorio contiene una solución integral compuesta por una API robusta y un cliente web moderno para la gestión de autenticación y visualización de datos según roles. Se opto por dar una mayor respuesta a la prueba tecnica que se nos planteo para el puesto de desarrollador full stack. Para ver solo la respuesta pedida ver el contenido de la carpeta backend. Por otro lado si se quiere ver el plus que le di revisar las dos propuestas (tanto frontend como backend). 

## 🌐 Demos en Línea (Despliegue)

El proyecto se encuentra desplegado y operativo en las siguientes plataformas, comprobar primero que la aplicación de Render este funcionando:

* **Frontend (Angular):** [\[https://prueba-tecnica-clerc-carvajal.vercel.app/login\]](https://prueba-tecnica-clerc-carvajal.vercel.app/login)
* **Backend API (Litestar):** [https://prueba-tecnica-clerc-carvajal.onrender.com/](https://prueba-tecnica-clerc-carvajal.onrender.com/)

> **Nota:** Al estar en capas gratuitas, la API puede tardar unos 60 segundos en "despertar" en la primera petición.

## 🏗️ Arquitectura del Proyecto

El sistema se divide en dos componentes principales que interactúan mediante una API REST:

1.  **Backend (`/backend`):** Construido con **Litestar** (Python). Gestiona la lógica de negocio, seguridad (hashing con Bcrypt), sesiones server-side y persistencia en base de datos (SQLAlchemy).
2.  **Frontend (`/frontend`):** Desarrollado en **Angular**. Ofrece una interfaz reactiva, consumo de servicios asíncronos y guardias de navegación según el rol del usuario, todo consultando a la api creada con Litestar.



## 👥 Credenciales de Acceso, para ambos casos

| Rol | Usuario | Contraseña | Alcance |
|------|---------|-----------|-----------|
| **Admin** | `jhon_doe` | `12345` | Acceso total a todos los registros. |
| **Supervisor** | `ana_torres` | `12345` | Visualiza supervisores y usuarios normales. |
| **Usuario** | `camila_navarro` | `12345` | Solo puede ver su propia información. |

## 🛠️ Guías de Instalación Local

Para ejecutar este proyecto en tu máquina, sigue las instrucciones detalladas en cada carpeta:

* 📖 [Configurar el Backend (Litestar)](./backend/README.md)
* 📖 [Configurar el Frontend (Angular)](./frontend/README.md)