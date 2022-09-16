from flask import Flask, render_template, redirect, session, request, abort
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import random

app = Flask(__name__)
app.secret_key = ".."
uri = os.environ.get('MONGO_DB_URI', "mongodb://127.0.0.1")
print(uri)
client = MongoClient(uri)
db = client.mafiance


@app.route("/")
def home_view():
    if not session.get('id'):
        session['id'] = random.randint(00000, 99999)
    return render_template("home.html", id=session.get('id'))


@app.route("/login")
def login_view():
    mensaje1 = request.args.get('mensaje1')
    return render_template("login.html", mensaje1=mensaje1)


@app.route("/loginpass")
def loginpass_view():
    mensaje2 = request.args.get('mensaje2')
    return render_template("loginpass.html", mensaje2=mensaje2)


@app.route("/login/admins")
def login_admins():
    adminEmail = request.args.get('email')
    if adminEmail == "":
        return redirect('/login?mensaje1=Ingresa el Email')

    adminDocument = db.admins.find_one({'email': adminEmail})

    if not adminDocument:
        return redirect('/login?mensaje1=El usuario no existe')

    session['admin'] = str(adminDocument['_id'])
    return redirect('/loginpass')


@app.route("/loginpass/admins")
def loginpass_admins():

    adminPassword = request.args.get('password')

    if adminPassword == "":
        return redirect('/loginpass?mensaje2=Ingresa la contraseña')

    # Arreglar que entienda 1 clave por usuario.
    adminDocument = db.admins.find_one({'password': adminPassword})

    if adminDocument['password'] != adminPassword:
        return redirect('/loginpass?mensaje2=La contraseña no es válida')

    return redirect('/index')


@app.route("/signin")
def signin_view():
    mensaje3 = request.args.get('mensaje3')
    return render_template("signin.html", mensaje3=mensaje3)


@app.route("/signin/new_user")
def signin_user():
    newEmail = request.args.get('email')
    newPassword = request.args.get('password')
    new_user_name = request.args.get('user')

    if newEmail == "":
        return redirect('/signin?mensaje3=Ingresa el Email')

    if newPassword == "":
        return redirect('/signin?mensaje3=Ingresa una Contraseña')

    if new_user_name == "":
        return redirect('/signin?mensaje3=Ingresa un nombre de Usuario')

    emailSplitted = newEmail.split('@')

    if len(emailSplitted) != 2 or emailSplitted[1] != 'gmail.com':

        return redirect('/signin?mensaje3=la dirección de correo no es válida, debe contener @gmail.com ó @hotmail.com')

    user = session.get('id')
    newDocument = {
        'email': newEmail,
        'password': newPassword,
        'user': new_user_name
    }
    newDocument['user_id'] = user
    db.users.insert_one(newDocument)  # Creamos documentos en la base de datos.

    return redirect('/finished')
    # Hacer que al iniciar sesión identifique el nuevo usuario.


@app.route("/finished")
def registration_view():
    return render_template("finished.html")


@app.route("/index")
def index_view():
    return render_template("index.html")


@app.route("/profile")
def profile_view():
    return render_template("profile.html")


@app.route("/p2pBuyer")
def p2pBuyer_view():
    return render_template("p2pBuyer.html")


@app.route("/p2pSeller")
def p2pSeller_view():
    return render_template("p2pSeller.html")


@app.route("/divisa")
def divisa_view():
    return render_template("divisa.html")
