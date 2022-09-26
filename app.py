from types import NoneType
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
    return render_template("home.html")


@app.route("/login")
def login_view():
    mensaje = request.args.get('mensaje')
    return render_template("login.html", mensaje=mensaje)


@app.route("/login/users")
def login_users():
    userEmail = request.args.get('email')
    userPassword = request.args.get('password')

    if userEmail == "":
        return redirect('/login?mensaje=Ingresa el Email o Nombre de usuario')
    if userPassword == "":
        return redirect('/login?mensaje=Ingresa la contraseña')

    # Forma fácil para buscar por email y tambien por el user registrado:
    userDocument = db.users.find_one({'email': userEmail})

    if not userDocument:
        userDocument = db.users.find_one({'user': userEmail})

    # userDocument = db.users.find_one({ '$or': [{'email': userEmail}, {'user': userEmail}]})

    if not userDocument:
        return redirect('/login?mensaje=El usuario no existe')
    # ----------------------------------
    if userDocument['password'] != userPassword:
        return redirect('/login?mensaje=La contraseña inválida')

    session['user_id'] = str(userDocument['_id'])

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

    if len(newPassword) < 8:
        return redirect('/signin?mensaje3=La contraseña debe contener 8 o más carácteres')

    if new_user_name == "":
        return redirect('/signin?mensaje3=Ingresa un nombre de Usuario')

    emailSplitted = newEmail.split('@')

    if len(emailSplitted) != 2 or emailSplitted[1] != 'gmail.com' != 'hotmail.com':

        return redirect('/signin?mensaje3=la dirección de correo no es válida, debe contener @gmail.com ó @hotmail.com')

    newUser = {
        'email': newEmail,
        'password': newPassword,
        'user': new_user_name
    }
    # Creamos documentos en la base de datos.
    newUserId = str(db.users.insert_one(newUser).inserted_id)
    # inserta el documento y devuelve el id del documento insertado con .inserted_id por eso se escribe abajo newUserId
    newWallet = {
        'currency': "MFC",
        'balance': 0.0,
        'user_id': newUserId,
    }
    db.wallets.insert_one(newWallet)

    session.pop('user_id', None)
    return redirect('/finished')

    # Tarea! Hacer que al iniciar sesión identifique al nuevo usuario.


@app.route("/finished")
def registration_view():
    return render_template("finished.html")


@app.route("/index")
def index_view():

    if not session.get('user_id'):
        return redirect('/')

    userId = session.get('user_id')

    actualBalance = db.wallets.find_one({'user_id': userId})

    return render_template("index.html", actualBalance=actualBalance)


@app.route("/profile")
def profile_view():

    if not session.get('user_id'):
        return redirect('/')
    return render_template("profile.html")


@app.route("/p2pBuyer")
def p2pBuyer_view():

    if not session.get('user_id'):
        return redirect('/')
    return render_template("p2pBuyer.html")


@app.route("/p2pSeller")
def p2pSeller_view():

    if not session.get('user_id'):
        return redirect('/')
    return render_template("p2pSeller.html")


@app.route("/divisa")
def divisa_view():

    if not session.get('user_id'):
        return redirect('/')
    return render_template("divisa.html")


@app.route("/orders")
def orders_view():
    if not session.get('user_id'):
        return redirect('/')
    return render_template("orders.html")


@app.route("/comercio")
def trade_view():
    if not session.get('user_id'):
        return redirect('/')
    return render_template("comercio_cripto.html")

# flask necesita a la ruta (/add/MFC/<id>) para despues def add(id):


@app.route("/add/MFC")
def add():
    if not session.get('user_id'):
        return redirect('/')
    # Cuando traemos un numero del formulario debemos convertirlo a numero porque viene como un string y no se
    # puede sumar con int() o float().
    amount = float(request.args.get('quantity'))
    userId = session.get('user_id')

    newTransaction = {
        'wallet_sender_id': 0,
        'wallet_receiver_id': userId,
        'amount': amount,
        'currency': "MFC",
        'created_at': "jueves"  # usar funcion date.now()
    }
    db.transactions.insert_one(newTransaction)
    # Agregar y aumentar el balance.
    wallet = db.wallets.find_one({'user_id': userId})
    print({'user_id': userId})

    if wallet:
        db.wallets.update_one(
            {'user_id': userId},
            {
                '$set': {'balance': wallet['balance'] + amount}
            }
        )
    else:
        return abort(404)

    return redirect("/index")
