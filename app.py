from flask import Flask, render_template, request, redirect, url_for, flash, session
from extencions import db
from models import Reclamacao, Usuario
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alunos_reclamacoes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'minha_chave'
db.init_app(app)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']
        if Usuario.query.filter_by(username=username).first():
            flash('Usuário já existe!')
            return redirect(url_for('cadastro'))
        usuario = Usuario(username=username)
        usuario.set_senha(senha)
        db.session.add(usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça login.')
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(username=username).first()
        if usuario and usuario.check_senha(senha):
            session['usuario_id'] = usuario.id
            flash('Login realizado com sucesso!')
            return redirect(url_for('pagina_principal'))
        else:
            flash('Usuário ou senha inválidos!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    flash('Logout realizado!')
    return redirect(url_for('login'))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/pagina_principal', methods=['GET', 'POST'])
def pagina_principal():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        nome_escola = request.form['nome_escola']
        categoria = request.form['categoria']
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        nome_reclamante = request.form.get('nome_reclamante')
        papel = request.form['papel']
        data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
        nova_reclamacao = Reclamacao(
            nome_escola=nome_escola,
            categoria=categoria,
            titulo=titulo,
            descricao=descricao,
            nome_reclamante=nome_reclamante,
            papel=papel,
            data=data
        )
        db.session.add(nova_reclamacao)
        db.session.commit()
        flash('Reclamação enviada com sucesso!')
        return redirect(url_for('pagina_principal'))
    reclamacoes = Reclamacao.query.order_by(Reclamacao.data.desc()).all()
    return render_template('index.html', reclamacoes=reclamacoes)

@app.route('/editar_reclamacao/<int:id>', methods=['GET', 'POST'])
def editar_reclamacao(id):
    reclamacao = Reclamacao.query.get_or_404(id)
    if request.method == 'POST':
        reclamacao.nome_escola = request.form['nome_escola']
        reclamacao.categoria = request.form['categoria']
        reclamacao.titulo = request.form['titulo']
        reclamacao.descricao = request.form['descricao']
        reclamacao.nome_reclamante = request.form.get('nome_reclamante')
        reclamacao.papel = request.form['papel']
        reclamacao.data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
        db.session.commit()
        flash('Reclamação editada com sucesso!')
        return redirect(url_for('pagina_principal'))
    return render_template('editar_reclamacao.html', reclamacao=reclamacao)

@app.route('/deletar_reclamacao/<int:id>', methods=['POST'])
def deletar_reclamacao(id):
    reclamacao = Reclamacao.query.get_or_404(id)
    db.session.delete(reclamacao)
    db.session.commit()
    flash('Reclamação deletada com sucesso!')
    return redirect(url_for('pagina_principal'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)