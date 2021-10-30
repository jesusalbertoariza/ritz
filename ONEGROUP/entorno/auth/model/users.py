import sqlite3
from sqlite3 import Error
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, TextAreaField, IntegerField, HiddenField, validators
from wtforms.validators import InputRequired, EqualTo, Length
from wtforms.fields.html5 import EmailField, TelField
from werkzeug.security import generate_password_hash, check_password_hash

def Db():
    con = None
    try: 
        con = sqlite3.connect("database.db") 
    except sqlite3.error as e: print(e)
    return con

#es necesario para la validacion propias para el email y el username 
def validate_username(Form, field):
    username = str(field.data)
    con        =  Db()
    cursor     = con.cursor()
    cursor.execute("SELECT username FROM users WHERE username=?",(username,))
    rows = cursor.fetchall()
    for r in rows:
        if username == r[0]:
            raise validators.ValidationError('Este usuario ya exite en la base de datos.')

def validate_email(Form, field):
    email = str(field.data)
    con        =  Db()
    cursor     = con.cursor()
    cursor.execute("SELECT email FROM users WHERE email=?",(email,))
    rows = cursor.fetchall()
    for r in rows:
        if email == r[0]:
            raise validators.ValidationError('Este email ya exite en la base de datos.')

class User(Form):

        def _create_pasword(password):
            return generate_password_hash(password) 
        
        def verify_pasword(passwordhash,password):
            return check_password_hash(passwordhash, password)

class RolUser():
    cliente = 'cliente'
    admin   = 'admin'
    super   = 'super'
   
class LoginForm(Form):

    username   = StringField('Usuario',validators = [
                             InputRequired(message=('Por favor ingrese su nombre!')),
                             Length(min=2, max=20, message='Ingrese un usuario válido')])
    password = PasswordField('Contraseña', validators=[InputRequired(),Length(min=3, max=20, message='Ingrese una contraseña válida')])
    #next = HiddenField('next')

class RegisterForm(Form):

    name       = StringField('Nombres',   validators=[InputRequired(),Length(min=2, max=40, message='Su nombre debe contener minimo 2 caracteres')])
    lastname   = StringField('Apellidos', validators=[InputRequired(),Length(min=2, max=40, message='Su apellido debe contener minimo 2 caracteres')])
    address    = StringField('Dirección', validators=[InputRequired()])
    celphone   = TelField('Celular',  validators=[InputRequired(),Length(min=3, max=250, message='Su celular debe contener minimo 6 caracteres')])

    username   = StringField('Usuario',validators = [
                             InputRequired(message=('Por favor ingrese su nombre!')),
                             Length(min=5, max=20, message='El usuario debe contener minimo 5 caracteres'), validate_username])

    email      = EmailField('email',validators = [
                        InputRequired(message = ('Por favor ingrese una dirección de correo!')),
                        Length(min=6, message='El email debe contener minimo 6 caracteres'),validate_email])
                        
    password   = PasswordField('Contraseña', validators=[
                        InputRequired(), 
                        EqualTo('confirm', message='Las constraseñas deben ser identicas.'),
                        Length(min = 6, message='La contraseña debe contener minimo 6 caracteres.')])

    confirm    = PasswordField('Repetir Contraseña')


class ChangePassword(Form):
    password = PasswordField('New Password', validators=[InputRequired(), EqualTo('confirm')])
    confirm  = PasswordField('Repeat Password')

class RoomForm(Form):
    nombre       = StringField('nombre',validators = [
                             InputRequired(message=('Por favor ingrese un nombre nombre!')),
                             Length(min=5, max=20, message='El nombre debe contener minimo 3 caracteres')])
    medidas      = StringField('medidas',validators = [
                             InputRequired(message=('El estado de la habitación es requerido!'))])                         
    numero       = IntegerField('numero',validators = [
                             InputRequired(message=('Por favor ingrese un numero de personas!'))])
    costo        = IntegerField('costo',validators = [
                             InputRequired(message=('Por favor ingrese el costo de la habitación!'))])
    descripcion  = TextAreaField('descripcion')


