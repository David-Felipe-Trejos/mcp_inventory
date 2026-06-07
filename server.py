"""
Servidor MCP para gestión de inventario.
Curso: Computación Cognitiva para Big Data
Tema: Conexión a herramientas externas mediante Model Context Protocol
"""

from mcp.server.fastmcp import FastMCP
import sqlite3
from database import init_db, DB_NAME

# Inicializar la base de datos al arrancar el servidor
init_db()

# Crear instancia del servidor MCP
mcp = FastMCP("InventarioDB")


def get_connection() -> sqlite3.Connection:
    """Retorna una conexión a la base de datos SQLite."""
    return sqlite3.connect(DB_NAME)


# ──────────────────────────────────────────────
# OPERACIONES CRUD
# ──────────────────────────────────────────────

@mcp.tool()
def crear_producto(nombre: str, categoria: str, cantidad: int, precio: float) -> str:
    """
    Crea un nuevo producto en el inventario.

    Args:
        nombre: Nombre del producto.
        categoria: Categoría del producto.
        cantidad: Cantidad disponible en inventario.
        precio: Precio unitario del producto.

    Returns:
        Mensaje de confirmación con el id asignado.
    """
    if cantidad < 0:
        return "Error: la cantidad no puede ser negativa."
    if precio < 0:
        return "Error: el precio no puede ser negativo."

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO productos (nombre, categoria, cantidad, precio) VALUES (?, ?, ?, ?)",
        (nombre, categoria, cantidad, precio),
    )

    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return f"Producto creado exitosamente con id={new_id}."


@mcp.tool()
def consultar_producto(id: int) -> dict:
    """
    Consulta un producto por su identificador.

    Args:
        id: Identificador único del producto.

    Returns:
        Diccionario con los datos del producto o mensaje de error.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
    row = cursor.fetchone()

    conn.close()

    if row:
        return {
            "id": row[0],
            "nombre": row[1],
            "categoria": row[2],
            "cantidad": row[3],
            "precio": row[4],
        }

    return {"error": f"Producto con id={id} no encontrado."}


@mcp.tool()
def actualizar_producto(id: int, cantidad: int) -> str:
    """
    Actualiza la cantidad disponible de un producto existente.

    Args:
        id: Identificador del producto a actualizar.
        cantidad: Nueva cantidad en inventario.

    Returns:
        Mensaje de confirmación o error.
    """
    if cantidad < 0:
        return "Error: la cantidad no puede ser negativa."

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (cantidad, id))
    rows_affected = cursor.rowcount

    conn.commit()
    conn.close()

    if rows_affected == 0:
        return f"Error: no se encontró el producto con id={id}."

    return f"Producto id={id} actualizado correctamente. Nueva cantidad: {cantidad}."


@mcp.tool()
def eliminar_producto(id: int) -> str:
    """
    Elimina un producto del inventario por su identificador.

    Args:
        id: Identificador del producto a eliminar.

    Returns:
        Mensaje de confirmación o error.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
    rows_affected = cursor.rowcount

    conn.commit()
    conn.close()

    if rows_affected == 0:
        return f"Error: no se encontró el producto con id={id}."

    return f"Producto id={id} eliminado correctamente."


@mcp.tool()
def listar_productos() -> list:
    """
    Lista todos los productos registrados en el inventario.

    Returns:
        Lista de diccionarios con los datos de cada producto.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos")
    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return []

    return [
        {
            "id": row[0],
            "nombre": row[1],
            "categoria": row[2],
            "cantidad": row[3],
            "precio": row[4],
        }
        for row in rows
    ]


# ──────────────────────────────────────────────
# HERRAMIENTAS COGNITIVAS Y ANALÍTICAS
# ──────────────────────────────────────────────

@mcp.tool()
def calcular_valor_total_inventario() -> dict:
    """
    Calcula el valor monetario total del inventario
    (suma de cantidad * precio para todos los productos).

    Returns:
        Diccionario con el valor total del inventario.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(cantidad * precio) FROM productos")
    total = cursor.fetchone()[0]

    conn.close()

    return {"valor_total_inventario": round(total, 2) if total else 0}


@mcp.tool()
def productos_agotados() -> list:
    """
    Retorna la lista de productos con cantidad igual a cero (agotados).

    Returns:
        Lista de productos agotados.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos WHERE cantidad = 0")
    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "nombre": row[1],
            "categoria": row[2],
            "cantidad": row[3],
            "precio": row[4],
        }
        for row in rows
    ]


@mcp.tool()
def producto_mas_costoso() -> dict:
    """
    Identifica el producto con el precio unitario más alto.

    Returns:
        Diccionario con los datos del producto más costoso.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos ORDER BY precio DESC LIMIT 1")
    row = cursor.fetchone()

    conn.close()

    if row:
        return {
            "id": row[0],
            "nombre": row[1],
            "categoria": row[2],
            "cantidad": row[3],
            "precio": row[4],
        }

    return {"error": "No hay productos registrados."}


@mcp.tool()
def estadisticas_inventario() -> dict:
    """
    Calcula estadísticas generales del inventario:
    total de productos, promedio de cantidad, promedio de precio y valor total.

    Returns:
        Diccionario con las estadísticas del inventario.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*), AVG(cantidad), AVG(precio), SUM(cantidad * precio) FROM productos"
    )
    total_productos, promedio_cantidad, promedio_precio, valor_total = cursor.fetchone()

    conn.close()

    return {
        "total_productos": total_productos or 0,
        "promedio_cantidad": round(promedio_cantidad, 2) if promedio_cantidad else 0,
        "promedio_precio": round(promedio_precio, 2) if promedio_precio else 0,
        "valor_total": round(valor_total, 2) if valor_total else 0,
    }


# ──────────────────────────────────────────────
# PUNTO DE ENTRADA
# ──────────────────────────────────────────────

if __name__ == "__main__":
    mcp.serve()
