from flask import Flask, render_template,request, redirect, url_for, flash
import requests
import json
from config import usuario, clave

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'una-clave-secreta-000001'

token = '' # Agregar Token
headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }

# URL general
URL_API = "http://127.0.0.1:8000/api/"

@app.route("/")
def hello_world():
    return "<h3>Consumo de API - Flask</h3>"

#####################
#       EJEMPLOS    #
##################### 
@app.route("/losestudiantes")
def los_estudiantes():
    """
    """
    r = requests.get("http://127.0.0.1:8000/api/estudiantes/",
            auth=(usuario, clave))
    estudiantes = json.loads(r.content)['results']
    numero_estudiantes = json.loads(r.content)['count']
    return render_template("losestudiantes.html", estudiantes=estudiantes,
    numero_estudiantes=numero_estudiantes)


@app.route("/lostelefonos")
def los_telefonos():
    """
    """
    r = requests.get("http://127.0.0.1:8000/api/numerost/",
            auth=(usuario, clave))
    datos = json.loads(r.content)['results']
    numero = json.loads(r.content)['count']
    return render_template("lostelefonos.html", datos=datos,
    numero=numero)


@app.route("/lostelefonosdos")
def los_telefonos_dos():
    """
    """
    r = requests.get("http://127.0.0.1:8000/api/numerost/",
            auth=(usuario, clave))
    datos = json.loads(r.content)['results']
    numero = json.loads(r.content)['count']
    datos2 = []
    for d in datos:
        datos2.append({'telefono':d['telefono'], 'tipo':d['tipo'],
        'estudiante': obtener_estudiante(d['estudiante'])})
    return render_template("lostelefonosdos.html", datos=datos2,
    numero=numero)

# funciones ayuda

def obtener_estudiante(url):
    """
    """
    r = requests.get(url, auth=(usuario, clave))
    nombre_estudiante = json.loads(r.content)['nombre']
    apellido_estudiante = json.loads(r.content)['apellido']
    cadena = "%s %s" % (nombre_estudiante, apellido_estudiante)
    return cadena

################
#   TALLER    #
################
@app.route("/edificios")
def listar_edificios():
    r = requests.get(f"{URL_API}edificios/", auth=(usuario, clave))
    
    edificios = json.loads(r.content)['results']
    numero_edificios = json.loads(r.content)['count']
    
    return render_template("edificios.html", edificios=edificios, numero_edificios=numero_edificios)

@app.route("/departamentos")
def listar_departamentos():
    r = requests.get(f"{URL_API}departamentos/", auth=(usuario, clave))
    
    departamentos = json.loads(r.content)['results']
    numero_departamentos = json.loads(r.content)['count']
    
    return render_template("departamentos.html", departamentos=departamentos, numero_departamentos=numero_departamentos)

@app.route("/crear_edificio", methods=['GET', 'POST'])
def crear_edificio():
    if request.method == 'POST':
        
        '''
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        ciudad = request.form['ciudad']
        tipo = request.form['tipo']
        '''
        
        data = {
            'nombre': request.form['nombre'],
            'direccion': request.form['direccion'],
            'ciudad': request.form['ciudad'],
            'tipo': request.form['tipo']
        }
        
        r = requests.post(f"{URL_API}edificios/", json=data, headers=headers)
        
        print(f"Status Code (Crear Edificio): {r.status_code}")
        
        nuevo_edificio = json.loads(r.content)
        
        flash(f"Edificio '{nuevo_edificio['nombre']} {nuevo_edificio['direccion']}' creado exitosamente!", 'success')
        
        return redirect(url_for('listar_edificios'))
    
    return render_template("crear_edificio.html")

@app.route("/crear_departamento", methods=['GET', 'POST'])
def crear_departamento():
    
    edificios_disponibles = []
        
    r_edificios = requests.get(f"{URL_API}/edificios" , headers=headers)
    edificios_disponibles = json.loads(r_edificios.content)['results']
    
    if request.method == 'POST':
        
        '''
        nombre_propietario = request.form['nombre_propietario']
        costo = request.form['costo']
        cuartos = request.form['cuartos']
        '''
        edificio_url = request.form['edificio']
        
        data = {
            'nombre_propietario': request.form['nombre_propietario'],
            'costo': request.form['costo'],
            'cuartos': request.form['cuartos'],
            'edificio': edificio_url
        }
        
        r = requests.post(f"{URL_API}departamentos/", data=data, auth=(usuario, clave))
        
        nuevo_depa = json.loads(r.content)
        
        flash(f"Nuevo departarmento creado exitosamente para '{nuevo_depa['nombre_propietario']}'", 'success')
        
        return redirect(url_for('listar_departamentos'))

    return render_template("crear_departamento.html", edificios=edificios_disponibles)

if __name__ == "__main__":
    app.run(debug=True)
