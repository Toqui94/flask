from flask import Flask, redirect, url_for, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Conexion DB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'coches'

#Almacenamiento de la conexión en una variable
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/informacion/')
def informacion():
    return render_template('informacion.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/insertar_coche', methods=['GET','POST'])
def insertar_coche():
    if request.method == 'POST':
        
        #Acceso a los campos del formulario
        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        ciudad = request.form['ciudad']
        
        #cargue de cursor SQL
        #conjunto de registros que devuelve una instrucción SQL
        cursor = mysql.connection.cursor()
        #Instrucción SQL
        cursor.execute("INSERT INTO coches VALUES(NULL, %s, %s, %s, %s)", (marca, modelo, precio, ciudad))
        #El commit finaliza la transacción actual
        cursor.connection.commit()        
        
        #Redirecciona al index luego de ejecutar el formulario       
        return redirect(url_for('index'))        
    
    return render_template('insertar_coche.html')

@app.route('/coches')
def coches():
    #cargue de cursor SQL
    #conjunto de registros que devuelve una instrucción SQL
    cursor = mysql.connection.cursor()
    #Consula SQL
    cursor.execute("SELECT * FROM coches")
    #Recorrido de la información almaceda en coches
    coches = cursor.fetchall()
    #Cierre de cursor
    cursor.close()
    
    return render_template('coches.html', coches=coches)

#Se debe recibir el id como parámetro
@app.route('/borrar-coche/<coche_id>')
def borrar_coche(coche_id):
    #cargue de cursor SQL
    cursor = mysql.connection.cursor()
    #Instrucción SQL con clausula WHERE
    cursor.execute(f"DELETE FROM coches WHERE id={coche_id}")
    #El commit finaliza la transacción actual
    mysql.connection.commit() 
    
    return redirect(url_for('coches')) 

#Se debe recibir el id como parámetro
@app.route('/editar-coche/<coche_id>', methods=['GET','POST'])
def editar_coche(coche_id):
    if request.method == 'POST':
        
        #Acceso a los campos del formulario
        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        ciudad = request.form['ciudad']
        
        #cargue de cursor SQL
        cursor = mysql.connection.cursor()
        #Instrucción SQL
        cursor.execute("""
            UPDATE coches
            SET marca=%s, modelo=%s, precio=%s, ciudad=%s WHERE id = %s
                       """, (marca, modelo, precio, ciudad, coche_id))
        #El commit finaliza la transacción actual
        cursor.connection.commit()        
               
        return redirect(url_for('coches'))     
    
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM coches WHERE id={coche_id}")
    #Recorrido de la información almaceda en coches
    coche = cursor.fetchall()
    #Cierre de cursor
    cursor.close()
    
    return render_template('insertar_coche.html', coche=coche[0]) 

@app.route('/insertar_usuario', methods=['GET','POST'])
def insertar_usuario():
    if request.method == 'POST':
        
        #Acceso a los campos del formulario
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        ciudad = request.form['ciudad']
        
        #cargue de cursor SQL
        #conjunto de registros que devuelve una instrucción SQL
        cursor = mysql.connection.cursor()
        #Instrucción SQL
        cursor.execute("INSERT INTO usuario VALUES(NULL, %s, %s, %s, %s)", (nombre, apellido, edad, ciudad))
        #El commit finaliza la transacción actual
        cursor.connection.commit()        
        
        #Redirecciona al index luego de ejecutar el formulario       
        return redirect(url_for('index'))        
    
    return render_template('insertar_usuario.html')

@app.route('/usuarios')
def usuarios():
    #cargue de cursor SQL
    #conjunto de registros que devuelve una instrucción SQL
    cursor = mysql.connection.cursor()
    #Consula SQL
    cursor.execute("SELECT * FROM usuario")
    #Recorrido de la información almaceda en coches
    usuarios = cursor.fetchall()
    #Cierre de cursor
    cursor.close()
    
    return render_template('usuarios.html', usuarios=usuarios)

#Se debe recibir el id como parámetro
@app.route('/borrar-usuario/<usuario_id>')
def borrar_usuario(usuario_id):
    #cargue de cursor SQL
    cursor = mysql.connection.cursor()
    #Instrucción SQL con clausula WHERE
    cursor.execute(f"DELETE FROM usuario WHERE id={usuario_id}")
    #El commit finaliza la transacción actual
    mysql.connection.commit() 
    
    return redirect(url_for('usuarios')) 

#Se debe recibir el id como parámetro
@app.route('/editar-usuario/<usuario_id>', methods=['GET','POST'])
def editar_usuario(usuario_id):
    if request.method == 'POST':
        
        #Acceso a los campos del formulario
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        ciudad = request.form['ciudad']
        
        #cargue de cursor SQL
        cursor = mysql.connection.cursor()
        #Instrucción SQL
        cursor.execute("""
            UPDATE usuario
            SET nombre=%s, apellido=%s, edad=%s, ciudad=%s WHERE id = %s
                       """, (nombre, apellido, edad, ciudad, usuario_id))
        #El commit finaliza la transacción actual
        cursor.connection.commit()        
               
        return redirect(url_for('usuarios'))     
    
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM usuario WHERE id={usuario_id}")
    #Recorrido de la información almaceda en usuarios
    usuario = cursor.fetchall()
    #Cierre de cursor
    cursor.close()
    
    return render_template('insertar_usuario.html', usuario=usuario[0]) 

@app.route('/consulta', methods=['GET','POST'])
def consulta():
    # Obtener todos los nombres de las columnas de la tabla usuario
    cursor = mysql.connection.cursor()
    cursor.execute("DESCRIBE usuario")
    columnas = cursor.fetchall()
    cursor.close()

    return render_template('consulta.html', columnas=columnas)

@app.route('/resultado', methods=['GET','POST'])
def resultado():
    # Obtener el nombre de la columna y el valor buscado desde el formulario
    columna = request.form['columna']
    valor = request.form['valor']

    # Construir la consulta SQL dinámicamente
    cursor = mysql.connection.cursor()
    query = f"SELECT * FROM usuario WHERE {columna} LIKE %s"
    cursor.execute(query, (f"%{valor}%",))
    resultado = cursor.fetchall()
    cursor.close()

    return render_template('resultado.html', resultado=resultado)

if __name__ == '__main__':
     app.run(debug=True)