import sqlite3
from sqlite3.dbapi2 import Error 
from flask_wtf import FlaskForm
from entorno.auth.model.users import User, LoginForm, RegisterForm, Db

class RoomController():

    id = ''
    nombre = ''
    numero = ''
    costo = ''
    medidas = ''
    descripcion = ''
    id_hotel = 1
    load = False

    def readRoom(): # Devuelve un objeto iterable tipo: sqlite3.Cursor
        try:
            con = Db()
            cursor = con.cursor()
            query = "SELECT * FROM habitaciones"
            rows = cursor.execute(query)
            con.commit()
            # for row in rows: #Mostrar datos en consola
            #     print(row)

            # print('Dev: Se ha leido la sala con exito.')
            return rows
        except Error:
            # print('Dev: Ha ocurrido un error')
            # print(Error)
            return None


    def createRoom(nombre = None,  medidas = None, numero = None, costo = None, estado = None, descripcion = None, id_hotel = 1):
        try:
            con = Db()
            cursor = con.cursor()
            query = """INSERT INTO habitaciones (nombre, medidas, numero, costo, descripcion, id_hotel) VALUES(?, ?, ?, ?, ?, ?)"""
            cursor.execute(query, (nombre, medidas, numero, costo, descripcion, id_hotel))
            con.commit()
            habitacion = cursor.lastrowid

            #se estblece el estado incial al crear la habitación
            cursor = con.cursor()
            query = """INSERT INTO estado_habitacion_has_habitaciones (estado_habitacion_id_estado_habitacion, habitaciones_id_habitaciones) VALUES(?, ?)"""
            cursor.execute(query, (habitacion, estado))
            con.commit()
            return True
        except Error as e:
            return  e
    
    def loadRoom(id):
        try:
            con = Db()
            cursor = con.cursor()
            query = "SELECT * FROM habitaciones WHERE id_habitaciones=?"
            rows = cursor.execute(query,(id,))
            con.commit()
            return rows
        except Error as e:
            return e

    def updateRoom(id = None, nombre = None,  medidas = None, numero = None, costo = None,descripcion = None):
            try: 
                con = Db()
                query = "UPDATE habitaciones SET nombre = ?, medidas = ?, numero = ?, descripcion = ?  WHERE id = '%s'"%id
                con.execute(query,(nombre, medidas, numero, costo, descripcion))
                con.conexion.commit()
                # print('Dev: Se ha actualizado la sala con exito.')
                return True
            except Error:
                # print('Dev: Ha ocurrido un error')
                # print(Error)
                return False

  