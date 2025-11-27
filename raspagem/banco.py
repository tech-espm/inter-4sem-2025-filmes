from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from config import conexao_banco

engine = create_engine(conexao_banco)



