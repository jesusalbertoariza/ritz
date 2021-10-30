import sqlite3
from sqlite3 import Error
from flask import Flask, session, flash, render_template, request, get_flashed_messages, redirect, url_for
from entorno.auth.model.users import User, LoginForm, RegisterForm, RoomForm, Db
from entorno.admin.roomController import RoomController
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['dash_cliente','dashboard','mi_perfil']:
        return redirect(url_for('login'))
    elif 'username' in session and request.endpoint in ['register','home']:
        return redirect(url_for('dashboard'))
    
@app.route('/')
def home():
    return render_template('public/index.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
  if 'username' in session:
      if session['perfil'] == 3:
        return redirect(url_for('dash_cliente'))
      elif session['perfil'] == 2 or session['perfil'] == 1:
        return redirect(url_for('dashboard'))  
  else:
    comment_form = LoginForm(request.form)
    if request.method == "POST":
        if comment_form.validate():
            username = request.form["username"]
            password = request.form["password"]
            con        =  Db()          
            cursor     = con.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?  LIMIT 1",(username,))
            rows = cursor.fetchall()
            if rows:
                for r in rows:
                    passwordhash = r[2]
                    verifypass = User.verify_pasword(passwordhash,password)
                    if (username == r[1]) and verifypass == True:
                        sucsess_message = 'Bienvenido {}'.format(username)
                        flash(sucsess_message)
                        session['id']          = r[0]
                        session['username']    = r[1]
                        session['email']       = r[3] 
                        session['status']      = r[4]
                        session['id_personal'] = r[6] 
                        session['perfil']      = r[7]   
                        if  session['perfil'] == 3:
                            return redirect(url_for('dash_cliente'))
                        elif session['perfil'] == 2 or session['perfil'] == 1:
                            return redirect(url_for('dashboard'))  
                    else:
                        error_message = 'Verifique su contraseña'
                        flash(error_message)  
            else:
                error_message = 'El usuario o la contraseña no es válido'
                flash(error_message)   

    return render_template('public/login.html', form = comment_form)   



@app.route('/register', methods=('GET', 'POST'))
def register():

    comment_form = RegisterForm(request.form)

    if request.method == "POST":
        if comment_form.validate():
            
            try:
                con        = Db()
                #inserción a la tabla personas             
                cursor     = con.cursor()
                name       = request.form["name"]
                lastname   = request.form["lastname"]
                sql        = """ INSERT INTO personas (nombre1, apellido1) VALUES(?,?)"""
                cursor.execute(sql,(name, lastname))
                con.commit()

                id_personas = cursor.lastrowid
                
                #inserción a la tabla ubicación
                cursor      = con.cursor()
                address     = request.form["address"]
                celphone    = request.form["celphone"]
                sql1        = """ INSERT INTO ubicacion (direccion_principal, celular_1, id_personal) VALUES(?,?,?)"""
                cursor.execute(sql1,(address, celphone, id_personas))
                con.commit() 

                #inserción a la tabla clientes
                cursor      = con.cursor()
                categorias  = 1
                sql2        = """ INSERT INTO clientes (id_personas,categorias) VALUES(?,?)"""
                cursor.execute(sql2,(id_personas,categorias))
                con.commit() 
               
                #inserción a la tabla users
                cursor      = con.cursor()
                username    = request.form["username"]
                password    = User._create_pasword(request.form["password"])
                email       = request.form["email"]
                id_perfiles = 3
                status      = 1
                sql3        = """ INSERT INTO users (id_personas, username, password, email, id_perfiles, status) VALUES(?,?,?,?,?,?)"""
                cursor.execute(sql3,(id_personas, username, password, email, id_perfiles, status))
                con.commit()  

                succcess_message = 'Su registro fue creado exitosamente'
                flash(succcess_message)
                return redirect(url_for('login'))   

            except Error as e:
                error_message = 'error al ingresar los datos'
                flash(error_message)
            
            finally: 
                if con:
                    cursor.close()
                    con.close()

    return render_template('public/register.html', form = comment_form)  


@app.route('/logout', methods=('GET', 'POST'))
def logout():
    session.clear()
    return redirect(url_for('login'))  


#clientes
@app.route('/dash_cliente', methods=('GET', 'POST'))
def dash_cliente():
    if 'perfil' in session:
        return render_template('private/cliente/dashboardcliente.html') 
    else:
        redirect(url_for('login'))  

#administración
@app.route('/admin/mi_perfil', methods=('GET', 'POST'))
def mi_perfil():
    if 'perfil' in session:
        return render_template('private/admin/mi_perfil.html')
    else:
        return redirect(url_for('login'))   
 
@app.route('/admin/dashboard', methods=('GET', 'POST'))
def dashboard():
    if 'perfil' in session:
        return render_template('private/admin/dashboard.html') 
    else:
        return redirect(url_for('login'))   
    
@app.route('/admin/estructuracion/habitaciones', methods=('GET', 'POST'))
def habitaciones():
    if 'perfil' in session:
        rows = RoomController.readRoom()
        return render_template('private/admin/panel_estructuracion.html', rows = rows) 
    else:
        return redirect(url_for('login'))   

@app.route('/admin/estructuracion/add_habitaciones', methods=('GET', 'POST'))
def add_habitacion():
    if 'perfil' in session:
        comment_form = RoomForm(request.form)
        if request.method == "POST":
            if comment_form.validate():
                try:
                    query = RoomController.createRoom(request.form["nombre"],request.form["medidas"],request.form["numero"], request.form["costo"], request.form["descripcion"])
                    if query == True:
                        succes_message = 'La habitación fue creada correctamente'
                        flash(succes_message)
                        return redirect(url_for('habitaciones'))
                    else:
                        error_message = query
                        flash(error_message)
                except Error as e:
                        error_message = 'Error al ingresar los datos'
                        flash(error_message)

        return render_template('private/admin/add_habitacion.html',form = comment_form) 
    else: 
        return redirect(url_for('login'))


@app.route('/admin/estructuracion/edit_habitaciones', methods= ['GET',] )
def editar_habitacion():
    #if 'perfil' in session:
        if 'id' in request.args:
              id = int(request.args['id'])
              comment_form = RoomForm(request.form)
              rows = RoomController.loadRoom(id)       
              return render_template('private/admin/edit_habitacion.html',form = comment_form, rows = rows) 
        else:
              return redirect(url_for('habitaciones'))
    #else:
        #return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=5000,debug=True) 