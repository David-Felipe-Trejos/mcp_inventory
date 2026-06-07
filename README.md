# 🗃️ MCP Inventory — Servidor MCP para Gestión de Inventario

Proyecto desarrollado para el curso **Computación Cognitiva para Big Data**.  
Implementa un servidor MCP en Python que expone operaciones CRUD y consultas analíticas sobre una base de datos SQLite de inventario.

---

## 📋 Requisitos

| Herramienta | Versión mínima |
|-------------|---------------|
| Python | 3.8+ |
| SQLite3 | Incluido en Python |
| fastmcp | última |

---

## 🚀 Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/<tu-usuario>/mcp_inventory.git
cd mcp_inventory

# 2. Crear y activar entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt
```

---

## ▶️ Ejecución

```bash
python server.py
```

El servidor MCP quedará disponible para que un cliente (p. ej. Claude Desktop) lo consuma a través del protocolo MCP.

---

## 🛠️ Herramientas disponibles

### CRUD

| Herramienta | Descripción |
|-------------|-------------|
| `crear_producto` | Agrega un nuevo producto al inventario |
| `consultar_producto` | Busca un producto por su `id` |
| `actualizar_producto` | Modifica la cantidad de un producto |
| `eliminar_producto` | Elimina un producto por su `id` |
| `listar_productos` | Lista todos los productos |

### Analíticas

| Herramienta | Descripción |
|-------------|-------------|
| `calcular_valor_total_inventario` | Suma `cantidad × precio` de todos los productos |
| `productos_agotados` | Lista productos con cantidad = 0 |
| `producto_mas_costoso` | Producto con el precio unitario más alto |
| `estadisticas_inventario` | Total, promedios y valor total del inventario |

---

## 📁 Estructura del proyecto

```
mcp_inventory/
├── server.py          # Servidor MCP con todas las herramientas
├── database.py        # Inicialización de la base de datos SQLite
├── requirements.txt   # Dependencias del proyecto
├── README.md          # Este archivo
└── inventory.db       # Base de datos (generada automáticamente)
```

---

## 🧪 Pruebas sugeridas

Desde un cliente MCP conectado al servidor, ejecutar:

1. Crear cinco productos de distintas categorías.
2. Consultar un producto por id.
3. Actualizar la cantidad de un producto.
4. Eliminar un producto.
5. Listar todos los productos.
6. Calcular el valor total del inventario.
7. Consultar productos agotados.
8. Identificar el producto más costoso.
9. Ver estadísticas generales del inventario.

---

## 📄 Licencia

MIT — libre uso académico.
