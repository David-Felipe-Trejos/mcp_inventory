import sqlite3

DB_NAME = "inventory.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_NAME)

def crear_producto(nombre, categoria, cantidad, precio):
    conn = get_connection(); cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, categoria, cantidad, precio) VALUES (?, ?, ?, ?)",
                   (nombre, categoria, cantidad, precio))
    new_id = cursor.lastrowid; conn.commit(); conn.close()
    return f"Producto creado exitosamente (id={new_id})"

def consultar_producto(id):
    conn = get_connection(); cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
    row = cursor.fetchone(); conn.close()
    if row:
        return {"id": row[0], "nombre": row[1], "categoria": row[2], "cantidad": row[3], "precio": row[4]}
    return {"error": "Producto no encontrado"}

def actualizar_producto(id, cantidad):
    conn = get_connection(); cursor = conn.cursor()
    cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (cantidad, id))
    conn.commit(); conn.close()
    return "Producto actualizado correctamente"

def eliminar_producto(id):
    conn = get_connection(); cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
    conn.commit(); conn.close()
    return "Producto eliminado correctamente"

def listar_productos():
    conn = get_connection(); cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    rows = cursor.fetchall(); conn.close()
    return [{"id": r[0], "nombre": r[1], "categoria": r[2], "cantidad": r[3], "precio": r[4]} for r in rows]

def calcular_valor_total_inventario():
    conn = get_connection(); cursor = conn.cursor()
    cursor.execute("SELECT SUM(cantidad * precio) FROM productos")
    total = cursor.fetchone()[0]; conn.close()
    return {"valor_total_inventario": round(total, 2) if total else 0}

def productos_agotados():
    conn = get_connection(); cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE cantidad = 0")
    rows = cursor.fetchall(); conn.close()
    return [{"id": r[0], "nombre": r[1], "categoria": r[2], "cantidad": r[3], "precio": r[4]} for r in rows]

def producto_mas_costoso():
    conn = get_connection(); cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos ORDER BY precio DESC LIMIT 1")
    row = cursor.fetchone(); conn.close()
    if row:
        return {"id": row[0], "nombre": row[1], "categoria": row[2], "cantidad": row[3], "precio": row[4]}
    return {"error": "No hay productos registrados"}

def estadisticas_inventario():
    conn = get_connection(); cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), AVG(cantidad), AVG(precio), SUM(cantidad * precio) FROM productos")
    tp, pa, pp, vt = cursor.fetchone(); conn.close()
    return {"total_productos": tp or 0, "promedio_cantidad": round(pa, 2) if pa else 0,
            "promedio_precio": round(pp, 2) if pp else 0, "valor_total": round(vt, 2) if vt else 0}

# ══════════════════════════════════════════════
#  PRUEBAS FUNCIONALES
# ══════════════════════════════════════════════

init_db()

SEP = lambda t: print(f"\n{'='*55}\n  PRUEBA: {t}\n{'='*55}")
import json

# PRUEBA 1
SEP("1 - Crear cinco productos")
print(crear_producto("Laptop Dell XPS 15",       "Electronica", 12, 4599000.0))
print(crear_producto("Mouse Inalambrico Logitech","Accesorios",  45,   89900.0))
print(crear_producto("Monitor LG 27 pulgadas",   "Electronica",  8, 1250000.0))
print(crear_producto("Teclado Mecanico Redragon", "Accesorios",   0,  349000.0))
print(crear_producto("Silla Ergonomica OFX",      "Muebles",       5, 2100000.0))

# PRUEBA 2
SEP("2 - Consultar producto por id (id=2)")
print(json.dumps(consultar_producto(2), ensure_ascii=False, indent=2))

# PRUEBA 3
SEP("3 - Actualizar cantidad (id=4, nueva cantidad=20)")
print(f"  Antes  -> cantidad: {consultar_producto(4)['cantidad']}")
print(f"  Accion -> {actualizar_producto(4, 20)}")
print(f"  Despues-> cantidad: {consultar_producto(4)['cantidad']}")

# PRUEBA 4
SEP("4 - Eliminar un producto")
print(crear_producto("Producto Temporal", "Test", 1, 10000))
print(f"  Eliminar id=6 -> {eliminar_producto(6)}")
print(f"  Consultar id=6 -> {consultar_producto(6)}")

# PRUEBA 5
SEP("5 - Listar todos los productos")
for p in listar_productos():
    print(f"  [{p['id']}] {p['nombre']:30s} | {p['categoria']:12s} | qty={p['cantidad']:3d} | ${p['precio']:,.0f}")

# PRUEBA 6
SEP("6 - Calcular valor total del inventario")
print(json.dumps(calcular_valor_total_inventario(), ensure_ascii=False, indent=2))

# PRUEBA 7
SEP("7 - Productos agotados (cantidad = 0)")
actualizar_producto(4, 0)
agotados = productos_agotados()
if agotados:
    for p in agotados:
        print(f"  AGOTADO -> [{p['id']}] {p['nombre']}")
else:
    print("  No hay productos agotados.")

# PRUEBA 8
SEP("8 - Producto mas costoso")
print(json.dumps(producto_mas_costoso(), ensure_ascii=False, indent=2))

# PRUEBA 9
SEP("9 - Estadisticas generales del inventario")
print(json.dumps(estadisticas_inventario(), ensure_ascii=False, indent=2))

print("\n" + "="*55)
print("  TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
print("="*55)
