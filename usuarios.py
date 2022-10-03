from flask_app import app
from flask_bcrypt import Bcrypt
from flask import request,flash,render_template,redirect,session
from flask_app.models.usuario import Usuario


bcrypt = Bcrypt(app)

@app.route('/') #*!Ruta raiz
def raiz():
    return render_template("registro_login.html")

@app.route('/add_usuario', methods=['POST'])
def register():
    # validar el formulario aquí...
    if not Usuario.validate_form(request.form):
        return redirect ('/')
    # if request.form['password'] != request.form['password_confirm']:
    #     flash('Passwords no coinciden')
    #     return redirect('/')

    # crear el hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    #poner pw_hash en el diccionario de datos
    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    # llama al @classmethod de guardado en Usuario
    user_id = Usuario.save(data)
    # almacenar id de usuario en la sesión
    session['user_id'] = user_id
    return redirect(f'/dashboard/{session["user_id"]}')

@app.route('/dashboard/<int:id>')
def dashboard(id):
    data = {
        "identificador":id
    }
    user = Usuario.get_usuario(data)
    print(user)
    todos_usuarios = Usuario.get_all()
    return render_template("dashboard.html", todos_usuarios=todos_usuarios, user=user)

@app.route('/login', methods=['POST'])
def login():
    # ver si el nombre de usuario proporcionado existe en la base de datos
    data = { "email" : request.form["email"] }
    user_in_db = Usuario.get_by_email(data)
    # usuario no está registrado en la base de datos
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # si obtenemos False después de verificar la contraseña
        flash("Invalid Email/Password")
        return redirect('/')
    # si las contraseñas coinciden, configuramos el user_id en sesión
    session['user_id'] = user_in_db.id
    # ¡¡¡Nunca renderices en una post!!!
    return redirect(f'/dashboard/{session["user_id"]}')

@app.route('/clearsession')
def clear():
    session.clear()
    return redirect('/')