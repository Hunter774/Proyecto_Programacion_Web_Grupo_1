from flask import Flask, render_template
from conexion import ConexionDB

db = ConexionDB(
    host="bdpw.mysql.database.azure.com",
    user="Hunter774575@bdpw",
    password="TuPassword123",
    db="tienda"
)


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# Ejemplo de endpoint para productos
@app.route("/productos")
def productos():
    db = ConexionDB("host_azure", "usuario", "password", "nombre_bd")
    cursor = db.obtener_cursor()
    cursor.execute("SELECT nombre, precio FROM productos")
    data = cursor.fetchall()
    return {"productos": data}

if __name__ == "__main__":
    app.run()
