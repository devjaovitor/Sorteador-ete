from flask import Flask, render_template, request, redirect
from data.db import connect
import random

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def homePage():
    conn = connect()
    cur = conn.cursor()

    sorteado = cadastrado = None
    aptos_sorteio = 0

    if request.method == "POST":
        acao = request.form.get("acao")

        if acao == "cadastrar":
            #Cadastro
            nome = request.form["nome"].title()
            telefone = request.form["telefone"]
            instituicao = request.form["instituicao"].title()

            cur.execute("Insert Into aluno (nome, telefone, instituicao, validado, sorteado) Values (?, ?, ?, 0, 0)", (nome, telefone, instituicao))

            conn.commit()

            pk = cur.lastrowid
            cadastrado = (pk, nome, telefone, instituicao)

        elif acao == "validar":
            #Validação
            validar = request.form["validar"]
            cur.execute("Update aluno Set validado = 1 Where num = ?", (validar,))

            conn.commit()

            return redirect("/")

        elif acao == "sorteio":
            usuarios = cur.execute("Select num, nome, telefone, instituicao From aluno Where validado = 1 and sorteado = 0").fetchall()
            if usuarios:
                #Sorteio
                sorteado = random.choice(usuarios)

                cur.execute("Update aluno Set sorteado = 1 Where num = ?", (sorteado[0],))
                conn.commit()

        elif acao == "inativar":
            numero = request.form["numero"]

            cur.execute("Delete from aluno where num = ?", (numero,))
            conn.commit()

            return redirect("/")

    aptos_sorteio = cur.execute("Select Count(*) From aluno Where validado = 1 and sorteado = 0").fetchone()[0] or 0
    
    #Filtro
    buscar = request.args.get("busca", "")

    if buscar:
        usuarios = cur.execute("""
            Select num, nome, telefone, instituicao, validado From aluno Where sorteado = 0 And nome Like ?
        """, ("%" + buscar + "%",)).fetchall()
        
    else:
        usuarios = cur.execute("""
            Select num, nome, telefone, instituicao, validado From aluno Where sorteado = 0
        """).fetchall()

    conn.close()
    return render_template("index.html", usuarios=usuarios, aptos_sorteio=aptos_sorteio, sorteado=sorteado, cadastrado=cadastrado)

if __name__ == "__main__":
    app.run()