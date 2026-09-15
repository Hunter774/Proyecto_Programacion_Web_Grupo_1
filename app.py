from flask import Flask, render_template, jsonify
from conexion import ConexionDB

db = ConexionDB(
    host="bdppw.mysql.database.azure.com",
    user="Hunter774575@bdppw"
    password="Darkhunter77*",
    db="xbits"
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/productos", methods=["GET"])
def get_productos():

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


if __name__ == "__main__":
    app.run()