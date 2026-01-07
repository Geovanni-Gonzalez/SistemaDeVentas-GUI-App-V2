# Sistema de Ventas con IA (V2 Ultra)

**Estudiante:** [Tu Nombre Completo]
**ID Estudiante:** [Tu ID]
**Estado del Proyecto:** 🏆 Finalizado (V2 Ultra - Full Features)

## 📋 Descripción

Sistema de Gestión de Ventas e Inventario desarrollado en Python con Tkinter. Esta versión "V2 Ultra" ha sido re-arquitectada profesionalmente para incluir bases de datos SQL, inteligencia artificial para predicción de stock y conectividad por correo electrónico.

## 🚀 Características Clave

### 1. Gestión de Datos Profesional (SQL)

- Migración completa de archivos de texto a **SQLite**.
- Integridad referencial en todas las transacciones.
- Soporte para miles de registros sin perdida de rendimiento.

### 2. Inteligencia Artificial (AI Analytics) 🤖

- **Motor de Predicción**: Algoritmo de regresión lineal que analiza el historial de ventas.
- **Smart Dashboard**: Alertas visuales que predicen cuándo se agotará un producto (e.g., "Agota en 3 días").

### 3. Conectividad y Reportes 📧

- **Generación de PDF**: Facturas profesionales generadas automáticamente.
- **Envío de Correos**: El sistema envía la factura .pdf al correo del cliente al instante.
- **Logging**: Sistema de registro de errores en `logs/` para soporte técnico.

### 4. Hiper-Conectividad (Fase 5) 🌐

- **Escáner de Código de Barras**: Integración con cámara web para lectura de productos en tiempo real (con modo manual de respaldo).
- **WhatsApp**: Comunicación automática con clientes para envío de comprobantes.
- **Sincronización Nube**: Exportación diaria de ventas compatible con Google Sheets.

## 🛠️ Tecnologías

- **Lenguaje**: Python 3.1x
- **GUI**: Tkinter + TTK (Tema Moderno)
- **Base de Datos**: SQLite3
- **Visualización**: Matplotlib (Dashboard)
- **Hardware**: OpenCV + Pyzbar (Escáner)
- **Reportes**: FPDF
- **Email**: SMTP Lib
- **Mensajería**: WhatsApp Web API

## ⚙️ Instalación y Ejecución

1. **Requisitos**:

    ```bash
    pip install matplotlib fpdf
    ```

2. **Ejecutar**:

    ```bash
    python programa/main.py
    ```

3. **Credenciales**:
    - **Usuario**: `admin`
    - **Contraseña**: `admin`

## 📂 Estructura del Proyecto

- `programa/src/`: Código Fuente
  - `analytics.py`: Motor de Inteligencia Artificial.
  - `database.py`: Gestor de Base de Datos.
  - `emailer.py`: Servicio de Correo.
  - `models.py`: Modelos de Datos.
  - `ui/`: Interfaz Gráfica.
- `programa/data/`: Base de datos (`sistema_ventas.db`).
- `documentacion/`: Manuales de Usuario y Técnico.
- `logs/`: Registros de ejecución.

## 📚 Documentación Técnica

Para detalles profundos sobre la arquitectura, el esquema de base de datos y la implementación de IA/Escáner, consulta el manual técnico oficial:

👉 **[Ver Documentación Técnica (Documentacion.md)](Documentacion.md)**
