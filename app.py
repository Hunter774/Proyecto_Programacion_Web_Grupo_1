from flask import Flask, render_template, jsonify
from conexion import ConexionDB

db = ConexionDB(
    host="bdppw.mysql.database.azure.com",
    user="Hunter774575",
    password="Darkhunter77*",
    db="xbits"
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/detalle/<int:id>")
def detalle(id):
    return render_template("detalle.html", id=id)

@app.route("/productos", methods=["GET"])
def get_productos():
    cursor = db.obtener_cursor()
    cursor.execute("""
        SELECT id_producto, nombre, descripcion, precio, imagen_url
        FROM Productos
        WHERE estado = 'activo'
    """)
    rows = cursor.fetchall()
    cursor.close()

    productos = []
    for row in rows:
        productos.append({
            "id": row["id_producto"],
            "nombre": row["nombre"],
            "descripcion": row["descripcion"],
            "precio": float(row["precio"]),
            "imagen": row["imagen_url"]
        })

    return jsonify(productos)


@app.route("/carrito")
def carrito():
    return render_template("carrito.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/terminos")
def terminos():
    return render_template("terminos.html")

@app.route("/privacidad")
def privacidad():
    return render_template("privacidad.html")


    cursor = db.obtener_cursor()

    cursor.execute("""
        SELECT id_producto, nombre, descripcion, precio, imagen_url
        FROM Productos
        WHERE estado = 'activo'
    """)

    rows = cursor.fetchall()

    productos = []

    for row in rows:
        productos.append({
            "id": row["id_producto"],
            "nombre": row["nombre"],
            "descripcion": row["descripcion"],
            "precio": float(row["precio"]),
            "imagen": row["imagen_url"]
        })

    cursor.close()

    return jsonify(productos)
#-----------------------------------------------------------------------

@app.route("/productos/<int:id>", methods=["GET"])
def get_producto(id):
    cursor = db.obtener_cursor()
    cursor.execute("""
        SELECT id_producto, nombre, descripcion, precio, imagen_url
        FROM Productos
        WHERE id_producto = %s AND estado = 'activo'
    """, (id,))
    row = cursor.fetchone()
    cursor.close()

    if row:
        producto = {
            "id": row["id_producto"],
            "nombre": row["nombre"],
            "descripcion": row["descripcion"],
            "precio": float(row["precio"]),
            "imagen": row["imagen_url"]
        }
        return jsonify(producto)
    else:
        return jsonify({"error": "Producto no encontrado"}), 404

@app.route("/carrito/<int:id>", methods=["GET"])
def get_carrito(id):
    cursor = db.obtener_cursor()
    cursor.execute("""
        SELECT cd.id_detalle, p.nombre, p.imagen_url, cd.cantidad, cd.precio_unitario
        FROM CarritoDetalle cd
        JOIN Carrito c ON cd.id_carrito = c.id_carrito
        JOIN Productos p ON cd.id_producto = p.id_producto
        WHERE c.id_usuario = %s
    """, (id,))
    rows = cursor.fetchall()
    cursor.close()

    carrito = []
    total = 0
    for row in rows:
        subtotal = float(row["precio_unitario"]) * row["cantidad"]
        total += subtotal
        carrito.append({
            "id_detalle": row["id_detalle"],
            "nombre": row["nombre"],
            "imagen": row["imagen_url"],
            "cantidad": row["cantidad"],
            "precio_unitario": float(row["precio_unitario"]),
            "subtotal": subtotal
        })

    return jsonify({"items": carrito, "total": total})

if __name__ == "__main__":
    app.run()


