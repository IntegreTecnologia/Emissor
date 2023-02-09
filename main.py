from flask import Flask, render_template, url_for
from database import db
from flask_migrate import Migrate
from usuarios import bp_usuarios
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

conexao = "sqlite:///../instance/integreemissor.sqlite"

app.config['SECRET_KEY'] = 'minha-chave'
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACKMODIFICATIONS'] = False
app.register_blueprint(bp_usuarios, url_prefix='/usuarios')

db.init_app(app)

Migrate = Migrate(app, db)

@app.route('/')
def index():
  return render_template('index.html')


app.run(host='0.0.0.0', port=81)
