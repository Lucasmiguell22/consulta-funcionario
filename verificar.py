from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Lukaoo618@",
    "database": "dori"
}

@app.route("/", methods=["GET", "POST"])
def home():
    mensagem = ""
    funcionario = None

    if request.method == "POST":
        re = request.form.get("re", type=int)
        nome = request.form.get("nome", type=str)

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM funcionarios WHERE id_funcionario = %s", (re,))
            funcionario = cursor.fetchone()

            if funcionario:
                if funcionario["nome_funcionario"] == nome:
                    mensagem = "Funcionário presente"
                else:
                    mensagem = "Funcionário ausente"
            else:
                mensagem = "RE ou nome inválido!"

            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            mensagem = f"Erro ao conectar ao banco: {err}"

    return render_template("index.html", mensagem=mensagem, funcionario=funcionario)

if __name__ == "__main__":
    app.run(debug=True)
