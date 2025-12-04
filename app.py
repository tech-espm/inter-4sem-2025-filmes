from flask import Flask, render_template, json, request, Response
import config
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

engine = create_engine(config.conexao_banco)

app = Flask(__name__)

@app.get('/')
def index():
    hoje = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/index.html', hoje=hoje)

@app.get('/sobre')
def sobre():
    return render_template('index/sobre.html', titulo='Sobre Nós')

@app.get('/dashboard')
def dashboard():
    return render_template('index/dashboard.html', titulo='Dashboard')

@app.get('/obterDados')
def obterDados():
    dados = {
        'top10': [],
        'top10generos': [],
        'top10anos': [],
    }

    with engine.begin() as conn:
        registros = conn.execute(text("select f.titulo, tmp.media from (select id_filme, avg(nota) media from ranking r group by id_filme) tmp inner join filme f on f.id = tmp.id_filme order by tmp.media desc limit 10"))
        for registro in registros:
            dados['top10'].append({
                'titulo': registro[0],
                'nota': registro[1]
            })

        registros = conn.execute(text("select g.nome, tmp.media from (select id_genero, avg(nota) media from ranking r inner join genero_filme gf on gf.id_filme = r.id_filme group by gf.id_genero) tmp inner join genero g on g.id = tmp.id_genero order by tmp.media desc limit 10"))
        for registro in registros:
            dados['top10generos'].append({
                'nome': registro[0],
                'nota': registro[1]
            })

        registros = conn.execute(text("select tmp.ano, tmp.media from (select f.ano, avg(r.nota) media from ranking r inner join filme f on f.id = r.id_filme group by f.ano) tmp order by tmp.media desc limit 10"))
        for registro in registros:
            dados['top10anos'].append({
                'ano': registro[0],
                'nota': registro[1]
            })

    return json.jsonify(dados)

@app.post('/criar')
def criar():
    dados = request.json
    print(dados['id'])
    print(dados['nome'])
    return Response(status=204)

if __name__ == '__main__':
    app.run(host=config.host, port=config.port)
