from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from config import conexao_banco

engine = create_engine(conexao_banco)

def salvar_filmes(filmes):
    print('CABRITA')
    with Session(engine) as sessao, sessao.begin():
        for filme in filmes:
            
            sessao.execute(text('''
                                INSERT INTO filme (titulo,duracao,ano,classificacao_etaria) 
                                VALUES
                                (:titulo,:duracao,:ano,:classificacao_etaria)
                                '''), filme)

