from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuração do Banco de Dados
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "site_acess.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa alertas de mudanças desnecessárias

# Inicialização do SQLAlchemy
db = SQLAlchemy(app)

# Modelo para salvar conexões
class ConnectionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    ip_address = db.Column(db.String(50), nullable=False)  # Endereço IP do visitante
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Data e hora do acesso

# Rota para a página inicial
@app.route('/')
def home():
    # Captura o IP do visitante
    visitor_ip = request.remote_addr

    # Registra a conexão no banco de dados
    new_log = ConnectionLog(ip_address=visitor_ip)
    db.session.add(new_log)
    db.session.commit()

    print(f"Conexão registrada: IP={visitor_ip}")
   
    # Renderiza o arquivo HTML "index.html" dentro da pasta "templates"
    return render_template('index.html')

# Rota para a página do sistema
@app.route('/system')
def system():
    return render_template('pSystem.html')


if __name__ == '__main__':
    with app.app_context():
      
        # Cria o banco de dados e a tabela, se não existirem
        db.create_all()
        
        # Remove todas as tabelas
        # db.drop_all()      


    app.run(debug=True)