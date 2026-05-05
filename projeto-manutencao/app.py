from flask import Flask, render_template, request, redirect
import pyodbc
import os

app = Flask(__name__)

def conectar_banco():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={os.getenv('DB_PASSWORD')};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

@app.route("/")
def index():
    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, equipamento, setor, tipo_manutencao, descricao, data_manutencao
            FROM manutencoes
            ORDER BY id DESC
        """)

        manutencoes = cursor.fetchall()
        conn.close()

        return render_template("index.html", manutencoes=manutencoes)

    except Exception as e:
        return f"Erro ao carregar dados: {e}"

@app.route("/adicionar", methods=["POST"])
def adicionar():
    try:
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

    except Exception as e:
        return f"Erro ao inserir dados: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)from flask import Flask, render_template, request, redirect
import pyodbc
import os

app = Flask(__name__)

def conectar_banco():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={os.getenv('servidorcp2pablo.database.windows.net')};"
        f"DATABASE={os.getenv('db-cp2-pablo-murilo')};"
        f"UID={os.getenv('adm-cp2-pablo-murilo')};"
        f"PWD={os.getenv('P2blo261628')};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

@app.route("/")
def index():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, equipamento, setor, tipo_manutencao, descricao, data_manutencao
        FROM manutencoes
        ORDER BY id DESC
    """)
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
