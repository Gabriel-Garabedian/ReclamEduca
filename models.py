from extencions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Reclamacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_escola = db.Column(db.String(150), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    nome_reclamante = db.Column(db.String(100), nullable=True)
    papel = db.Column(db.String(50), nullable=False)
    data = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Reclamacao {self.titulo} - Escola {self.nome_escola}>'