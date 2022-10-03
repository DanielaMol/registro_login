from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
import re # el módulo regex
# crea un objeto de expresión regular que usaremos más adelante
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Usuario:
    db_name="esquema_login_registro"

    def __init__( self , data ):
        self.id = data['id']
        self.nombre = data['first_name']
        self.apellido = data['last_name']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def get_all(cls): #*!metodo para obtener todos los datos
        query = "SELECT * FROM usuario;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        registro_usuarios =[]
        for x in results:
            registro_usuarios.append(cls(x))
        return registro_usuarios
    
    @classmethod
    def get_usuario(cls, data): #*!obtenemos un usuario mediante su id
        query = "SELECT * FROM usuario WHERE id=%(identificador)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data )
        return cls(result[0])

    @classmethod
    def get_by_email(cls,data): #*!recibir por correo electronico
        query = "SELECT * FROM usuario WHERE email = %(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        # no se encontró un usuario coincidente
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def save(cls,data): #*!guardar informacion en la bd
        query = "INSERT INTO usuario (first_name,last_name,email, password) VALUES (%(nombre)s,%(apellido)s,%(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_form(registro): #*!validamos la informacion que ingresa el usuario en el formulario
        # otros métodos Burger más allá
        # los métodos estáticos no tienen self o cls pasados a los parámetros
        # necesitamos tomar un parámetro para representar nuestra hamburguesa
        correo = {
            'email':registro['email']
        }
        is_valid = True # asumimos que esto es true
        if len(registro['nombre']) < 4:
            flash("Nombre debe contener al menos 2 caracteres.")
            is_valid = False
        if len(registro['apellido']) < 4:
            flash("Apellido debe contener al menos 2 caracteres.")
            is_valid = False
        if not EMAIL_REGEX.match(correo['email']): 
            flash("Direccion de correo electronico no valida!")
            is_valid = False
        elif Usuario.get_by_email(correo):
            flash("Direccion de correo ya existente!")
            is_valid = False
        if len(registro['password']) < 8:
            flash("Contraseña insegura: debe tener al menos 8 caracteres")
            is_valid = False
        if registro['password'] != registro['password_confirm']:
            flash('Passwords no coinciden')
            is_valid = False
        return is_valid