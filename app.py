from flask import Flask
from flask import request
import pymysql
import pymysql.cursors
from flask_cors import CORS

#Conectando no banco de dados
db = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='sistema',
    cursorclass=pymysql.cursors.DictCursor
)

#Criando nosso "app" para criarmos a API CRUD
app = Flask(__name__)
CORS(app)

#READ
@app.route("/usuarios", methods=["GET"])
def ler_usuario():
    cursor = db.cursor()

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    return usuarios

#CREATE
@app.route("/usuarios", methods=["POST"])
def criar_usuario():
    cursor = db.cursor()
    body = request.get_json()

    cursor.execute(f"INSERT INTO usuarios (nome, data_nascimento, senha) VALUE ('{body['nome']}', '{body['data_nascimento']}', '{body['senha']}')")
    db.commit()

    return "Criando Usuário"

#UPDATE
@app.route("/usuarios/<id_usuario>", methods=["PUT"])
def atualizar_usuario(id_usuario):
    cursor = db.cursor()
    body = request.get_json()

    cursor.execute(f"""
        UPDATE usuarios
        SET senha = '{body['senha']}',
        nome = '{body['nome']}',
        data_nascimento = '{body['data_nascimento']}'
        where id = {id_usuario};
    """)

    db.commit()

    return f"ATUALIZANDO USUÁRIO {id_usuario}"

#DELETE
@app.route("/usuarios/<id_usuario>", methods=["DELETE"])
def deletar_usuario(id_usuario):

    cursor = db.cursor()

    cursor.execute(f"""
        DELETE FROM usuarios
        where id = {id_usuario};
    """)

    db.commit()

    return f"Deletando Usuário {id_usuario}"

if __name__ == '__main__':
    app.run(debug=True)