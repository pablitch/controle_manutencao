from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

def conectar_banco():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=servidorcp2pablo.database.windows.net;"
        "DATABASE=db-cp2-pablo-murilo;"
        "UID=adm-cp2-pablo-murilo;"
        "PWD=P@blo261628;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )

@app.route("/")
def index():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT id, equipamento, setor, tipo_manutencao, descricao, data_manutencao FROM manutencoes ORDER BY id DESC")
    manutencoes = cursor.fetchall()
    conn.close()
    return render_template("index.html", manutencoes=manutencoes)

@app.route("/adicionar", methods=["POST"])
def adicionar():
    equipamento = request.form["equipamento"]
    setor = request.form["setor"]
    tipo = request.form["tipo_manutencao"]
    descricao = request.form["descricao"]

    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO manutencoes (equipamento, setor, tipo_manutencao, descricao)
        VALUES (?, ?, ?, ?)
    """, equipamento, setor, tipo, descricao)

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
