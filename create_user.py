from models import db, User
from app import app

if __name__ == '__main__':
    with app.app_context():
        username = input("Username: ")
        password = input("Senha: ")
        u = User(username=username)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        print("Usuário criado com sucesso!")
