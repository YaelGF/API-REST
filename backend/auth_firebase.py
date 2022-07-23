import email
import hashlib  # importa la libreria hashlib
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyCqcAsOlCtnuCEmUIUgJJvTeHg9n2xjCg4",
    "authDomain": "loginapirest-b1c29.firebaseapp.com",
    "databaseURL": "https://loginapirest-b1c29-default-rtdb.firebaseio.com/",
    "projectId": "loginapirest-b1c29",
    "storageBucket": "loginapirest-b1c29.appspot.com",
    "messagingSenderId": "364265836121",
    "appId": "1:364265836121:web:09a406b3328d87323f6b48",
    "measurementId": "G-DVS09D026Q"
  };

email = "1719110736@utectulancingo.edu.mx"

password_b = hashlib.md5("user".encode())
password = password_b.hexdigest()


firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()
db = firebase.database()

def login_forParams():
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except:
        print("Error")
        

def login():
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print("Token: " + user['idToken'])
    except Exception as e:
        print(e)

def register():
    try:
        user = auth.create_user_with_email_and_password(email, password)
        auth.send_email_verification(user['idToken'])
    except:
        print("Error en registro") 

def logout():
    auth.signOut()
    print("Sesión cerrada")

def reset_password():
    auth.send_password_reset_email(email)
    print("Se ha enviado un correo para restablecer la contraseña")

def delete_account(user):
    try:
        auth.delete_user_account(user['idToken'])
    except:
        print("Error en eliminación de cuenta")

def role(user):
    try:
        data = {
            "nombre": user["email"],
            "role": "admin"
            }
        print(user['email'])
        password_natural = hashlib.md5(user["localId"].encode())
        password_new = password_natural.hexdigest()
        db.child("users/").child(password_new).set(data)
    except Exception as e:
        print(e)
        print("Error en asignación de rol")


if __name__ == "__main__":
    #delete_account(login_forParams())
    #reset_password()
    #change_password()
    #register()
    #login()
    role(login_forParams())