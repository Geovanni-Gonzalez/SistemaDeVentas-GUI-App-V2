# Recomendaciones y Mejoras Futuras

Este documento resume las áreas de oportunidad para llevar el "Sistema de Ventas V2" al siguiente nivel profesional.

## 1. Arquitectura y Persistencia

- **Migración a SQLite**: Actualmente el sistema usa archivos de texto (`.txt`) que son propensos a corrupción y lentos con muchos datos.
  - *Mejora*: Implementar una base de datos relacional ligera como SQLite. Esto facilitaría consultas complejas (e.g., "Ventas por mes") mediante SQL en lugar de filtrar listas en Python.
- **Capa de Servicios**: La lógica de negocio (e.g., validación de stock negativo) está mezclada en la UI (`GenericCrudFrame`).
  - *Mejora*: Crear una capa `services/` (ej. `InventoryService.py`) que maneje las reglas de negocio, desacoplando la interfaz de la lógica.

## 2. Funcionalidad Avanzada

- **Roles y Permisos**: Actualmente todos son `admin`.
  - *Mejora*: Diferenciar entre `Vendedor` (solo factura) y `Administrador` (gestion inventario y usuarios).
- **Envío de Correos**: Integrar `smtplib`.
  - *Mejora*: Enviar automáticamente el PDF de la factura al correo del cliente registrado al finalizar la venta.
- **Configuración Dinámica**:
  - *Mejora*: Una pantalla de "Configuración" para editar el IV (Impuesto), nombre de la empresa y logo del reporte sin tocar código.

## 3. Calidad de Código (DevOps)

- **Unit Testing**: No existen pruebas automáticas.
  - *Mejora*: Integrar `unittest` o `pytest` para verificar que el cálculo de totales y la reducción de stock funcionen siempre correctamente ante cambios futuros.
- **Manejo de Errores Robusto**:
  - *Mejora*: Implementar un sistema de *logging* (`logging` module) que guarde errores en un archivo `app.log` para depuración post-cierre.

## 4. Interfaz Gráfica (UX)

- **Modo Oscuro/Claro**: Aunque el tema es moderno, permitir cambiar el esquema de colores en tiempo real.
- **Dashboard Interactivo**: Permitir hacer clic en las barras del gráfico para ver el detalle de los productos.

---
**Plan de Acción Sugerido:**

1. Priorizar **SQLite**: Es el cambio que más valor técnico añade.
2. Implementar **Logging**: Es vital para soporte.
3. Añadir **Envío de Correos**: Alto impacto visual para el usuario final.
