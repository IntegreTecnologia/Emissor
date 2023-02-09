
from flask import Blueprint, flash
from flask import render_template, request, redirect
from models import Usuario
from database import db


import mysql.connector as mysql
import requests
import json
import os

bp_usuarios = Blueprint("usuarios", __name__, template_folder = "templates")
AuthorizationIwa = os.environ['AuthorizationIwa']
uspwmy = os.environ['uspwmy']



@bp_usuarios.route('/create', methods=['GET', 'POST'])
def create():
  if request.method == 'GET':
    return render_template('usuarios_create.html')
  if request.method == 'POST':
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    csenha = request.form.get('csenha')

    usuario = Usuario(nome, email, senha)
    if senha == csenha:
      db.session.add(usuario)
      db.session.commit()
      flash("Dados inseridos no BD")
      return render_template('usuarios_create.html', usuario=usuario)
    else:
      flash("Erro! Senhas não conferem.")
      return render_template('usuarios_create.html', usuario=usuario)


@bp_usuarios.route('/recovery')
def recovery():
  usuarios = Usuario.query.all()
  return render_template('usuarios_recovery.html', usuarios=usuarios)


@bp_usuarios.route('/update/<int:id>', methods=['GET', 'POST'])
def upadte(id):
  usuario = Usuario.query.get(id)
  if request.method == 'GET':
    return render_template('usuarios_update.html', usuario=usuario)

  if request.method == 'POST':
    nome = request.form.get('nome')
    email = request.form.get('email')
    usuario.nome = nome
    usuario.email = email
    db.session.add(usuario)
    db.session.commit()
    flash("Dados atualizados no BD")
    return render_template('usuarios_update.html', usuario=usuario)
    #return "Dados atualizados no BD"


@bp_usuarios.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
  usuario = Usuario.query.get(id)
  if request.method == 'GET':
    return render_template('usuarios_delete.html', usuario=usuario)

  if request.method == 'POST':
    db.session.delete(usuario)
    db.session.commit()
    flash("Dados excluidos no BD")
    return render_template('usuarios_delete.html', usuario=usuario)


@bp_usuarios.route('/emitenf', methods=['GET', 'POST'])
def emitenf():

  if request.method == 'GET':
    return render_template('emite_notafiscal.html')

  if request.method == 'POST':
    cmboperacaofiscal = request.form.get('cmboperacaofiscal')
    cpfcnpjid = request.form.get('cpfcnpjid')
    nomeparticipante = request.form.get('nomeparticipante')
    codparticipante = request.form.get('cmbparticipante')
    
    
    try:

        if request.form.get('cpfcnpjid') or request.form.get('nomeparticipante'):
          conexaobd = mysql.connect(host='pythondjango.mysql.dbaas.com.br',database='pythondjango', user='pythondjango', password=uspwmy)
  
          if len(cpfcnpjid.strip()) > 0:
            comandosql = "SELECT codParticipante, xNome_dest FROM pythondjango.tabParticipante where CPF_dest = '" + cpfcnpjid + "' or CNPJ_dest = '" + cpfcnpjid + "' or idEstrangeiro = '" + cpfcnpjid + "' order by xNome_dest"
          elif len(nomeparticipante.strip()) > 0:
            comandosql = "SELECT codParticipante, xNome_dest FROM pythondjango.tabParticipante where xNome_dest like '%" + nomeparticipante + "%' order by xNome_dest"
  
        
          mycursor = conexaobd.cursor(buffered=True)
          mycursor.execute(comandosql)
          result = mycursor.fetchall()
  
          qtde = mycursor.rowcount
        
          conexaobd.commit()
          conexaobd.close()
        
          flash("etapa1")
          return render_template('emite_notafiscal.html', result=result, qtde=qtde)

        if request.form.get('cmbparticipante'):

            conexaobd = mysql.connect(host='pythondjango.mysql.dbaas.com.br',database='pythondjango', user='pythondjango', password=uspwmy)

            mycursor = conexaobd.cursor(buffered=True)
            mycursor.execute("SELECT codOperacaoFiscal_NFSe, desOperacaoFiscal FROM pythondjango.tabOperacaoFiscal_NFSe")
            result = mycursor.fetchall()

            mycursor = conexaobd.cursor(buffered=True)
            mycursor.execute("SELECT * FROM pythondjango.tabParticipante where codParticipante=" + codparticipante)
            result2 = mycursor.fetchall()
          
            conexaobd.commit()
            conexaobd.close()

            flash("etapa2")
            flash(codparticipante)
            flash(result2[0][3])          
            return render_template('emite_notafiscal.html', result=result, result2=result2, op=result2[0][19])

        if request.form.get('cmboperacaofiscal'):

            flash("etapa3")
            return render_template('emite_notafiscal.html', aloha='Boto fé')          
          
    except ValueError:
        flash("Deu ruim")
        return render_template('emite_notafiscal.html', numeronf=numeronf, serienf=serienf)
    
    

@bp_usuarios.route('consultanf', methods=['GET', 'POST'])
def consultanf():

  if request.method == 'GET':
    clientesIwa = [{"nomecliente":"Ra Radiologia", "chaveemissor": "0dr9DK4Z85o5STDyav5ZlmRY53A1sah4"}, {"nomecliente":"Integre tecnologia", "chaveemissor": "VJmLpmCrYlrOw34YuHZtZdBYIO75I0l9"},{"nomecliente":"RADIOGRAPH", "chaveemissor": "sRJoJa6RecMwH96OQgy3UY3RySJhBqXF"}]
    
    return render_template('consulta_notafiscal.html', clientesIwa=clientesIwa)

  if request.method == 'POST':
    chaveemissor = request.form.get('chaveemissor')
    numeronf = request.form.get('nnf')
    serienf = request.form.get('serie')
    
    try:
        api_url = "http://www.integre.net.br/iwa/Api/NFSe/Consultar"
        headers = {'Content-Type': 'application/json', 'Authorization': AuthorizationIwa}
        body = {"nNF": numeronf, "serie": serienf, "nomChaveAcesso": chaveemissor}        
        response = requests.post(api_url, json=body, headers=headers)
      
        dados = json.dumps(response.json())
        if dados[0] == "[":  
          dadosjson = json.loads(dados[1:-1])
        else:
          dadosjson = json.loads(dados)
        
        flash("OK")
        return render_template('consulta_notafiscal.html', dadosjson=dadosjson )
    except ValueError:
        flash("Deu ruim")
        return render_template('consulta_notafiscal.html', numeronf=numeronf, serienf=serienf)
    