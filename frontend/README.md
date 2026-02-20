# Frontend - Angular Client

Interfaz de usuario moderna para el consumo de la API de gestión de datos.

## 🛠 Requisitos previos
- **Node.js**: v18.0 o superior
- **Angular CLI**: Instalado globalmente (`npm install -g @angular/cli`)

## 🚀 Instalación Local

1.  **Entrar a la carpeta del proyecto:**
    ```bash
    cd frontend
    ```
2.  **Instalar dependencias:**
    ```bash
    npm install
    ```
3.  **Configuración de la API:**
    Asegúrate de que el archivo de entorno (`src/environments/environment.ts`) apunte a la URL de tu backend local:
    ```typescript
    export const environment = {
      apiUrl: 'http://localhost:8000'
    };
    ```
4.  **Levantar el servidor de desarrollo:**
    ```bash
    ng serve
    ```
    Navega a `http://localhost:4200/`.
