from roomController import RoomController
import sqlite3


def conectar():
    con = None
    try: 
        con = sqlite3.connect("database.db") 
    except sqlite3.error as e: print(e)
    return con


if __name__ == '__main__':
    conexion = conectar()

    """ 
        * Data Test *

        - Sala 1
        - 30x30
        - Esta no es una descripcion.
        - [Defecto]
        - [Defecto]
        - [Defecto]
    """
    room = RoomController( conexion=conexion )

    room.readRoom()

    conexion.close()