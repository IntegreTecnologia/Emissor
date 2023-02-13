
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

  # GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET
  if request.method == 'GET':
    return render_template('emite_notafiscal.html')

  if request.method == 'POST':
    cpfcnpjid = request.form.get('cpfcnpjid')
    nomeparticipante = request.form.get('nomeparticipante')
    codparticipante = request.form.get('cmbparticipante')

    

    # ETAPA 1 ETAPA 1 ETAPA 1 ETAPA 1 ETAPA 1 ETAPA 1 ETAPA 1 ETAPA 1 ETAPA 1
    try:

        # O USUÁRIO DIGITOU ALGUM CRITERIO NA PESQUISA
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

        # O USUÁRIO NÃO DIGITOU NENHUM CRITERIO NA PESQUISA - TRAZ OS 10 PRIMEIROS REGISROS 
#        elif not(request.form.get('cmbparticipante')) and not(request.form.get('cmboperacaofiscal')):
#          conexaobd = mysql.connect(host='pythondjango.mysql.dbaas.com.br',database='pythondjango', user='pythondjango', password=uspwmy)
#  
#          comandosql = "SELECT codParticipante, xNome_dest FROM pythondjango.tabParticipante limit 10"
#            
#          mycursor = conexaobd.cursor(buffered=True)
#          mycursor.execute(comandosql)
#          result = mycursor.fetchall()
#  
#          qtde = mycursor.rowcount
#
#          conexaobd.commit()
#          conexaobd.close()
#        
#          flash("etapa1")
#          return render_template('emite_notafiscal.html', result=result, qtde=qtde)
        

        #ETAPA 2 ETAPA 2 ETAPA 2 ETAPA 2 ETAPA 2 ETAPA 2 ETAPA 2 ETAPA 2 ETAPA 2 
        elif request.form.get('cmbparticipante'):

            conexaobd = mysql.connect(host='pythondjango.mysql.dbaas.com.br',database='pythondjango', user='pythondjango', password=uspwmy)

            mycursor = conexaobd.cursor(buffered=True)
            mycursor.execute("SELECT codOperacaoFiscal_NFSe, desOperacaoFiscal ,replace(ValAliqISS,'.',',') as ValAliqISS,replace(ValAliqPIS,'.',',') as ValAliqPIS,replace(ValAliqCOFINS,'.',',') as ValAliqCOFINS,replace(ValAliqIR,'.',',') as ValAliqIR,replace(ValAliqCSLL,'.',',') as ValAliqCSLL,indISSRet,flgRetencaoPIS,flgRetencaoCofins,flgRetencaoIRRF,flgRetencaoCSLL FROM pythondjango.tabOperacaoFiscal_NFSe")
            result = mycursor.fetchall()

            mycursor = conexaobd.cursor(buffered=True)
            mycursor.execute("SELECT * FROM pythondjango.tabParticipante as a INNER JOIN tabMunicipio as c on a.codMunicipio = c.cMun where codParticipante=" + codparticipante)
            result2 = mycursor.fetchall()

            mycursor = conexaobd.cursor(buffered=True)
            mycursor.execute("SELECT * FROM pythondjango.tabServico order by cProd")
            result3 = mycursor.fetchall()          
          
            conexaobd.commit()
            conexaobd.close()

            flash("etapa2")
            flash(codparticipante)
            flash(result2[0][3])          
            return render_template('emite_notafiscal.html', result=result, result2=result2, result3=result3, op=result2[0][19])

        # ETAPA 3 ETAPA 3 ETAPA 3 ETAPA 3 ETAPA 3 ETAPA 3 ETAPA 3 ETAPA 3 ETAPA 3
        elif request.form.get('cmboperacaofiscal'):
            cpfParticipante = request.form.get('cpfParticipante')
            cnpjParticipante = request.form.get('cnpjParticipante')
            nomeParticipante = request.form.get('nomeParticipante')
            flash("etapa3")
            return render_template('emite_notafiscal.html', aloha=cnpjParticipante + nomeParticipante)    

        # ETAPA 4 ETAPA 4 ETAPA 4 ETAPA 4 ETAPA 4 ETAPA 4 ETAPA 4 ETAPA 4 ETAPA 4
        elif request.form.get('numeroNfe'):
            chaveemissor = os.environ['chaveemissor']

            try:
                api_url = "http://www.integre.net.br/iwa/api/NFSe/Enviar"
                headers = {'Content-Type': 'application/json', 'Authorization': AuthorizationIwa}
                body = { 
   "tipoNota":"NFSe",
   "nomChaveAcesso": chaveemissor,
   "codOperacaoFiscal":"1",
   "nNF":"",
   "dhEmi":"2023-02-12T08:27:00.501Z",
   "idEstrangeiro":"11",
   "xNome_dest":"TESTE PESSOA FISICA",
   "nomFantasia":"CAIXA DE ASSIST. DOS EMPREGADOS DA EMPRESA BRAS. DE PESQ. AG",
   "xLgr_dest":"SAIN PARQUE DE ESTACAO BIOLOGICA ED. SEDE",
   "nro_dest":"0",
   "xCpl_dest":"",
   "xBairro_dest":"BRASILIA",
   "codMunicipio":"5300108",
   "xMun_dest":"BRASILIA",
   "codPais":"1058",
   "fone_dest":"6134484091",
   "infCpl":"",
   "xEmail_dest":"",
   "dhSaiEnt":"2023-02-12T08:2:00:25.599Z",
   "Cod_dest":"",
   "CNPJ_dest":"",
   "CPF_dest":"52652840100",
   "IM_dest":"",
   "IE_dest":"",
   "UF_dest":"DF",
   "CEP_dest":"70770901",
   "Servicos":[ 
      { 
         "cProd":1,
         "vProd":"1.00",
         "qCOM":"1",
         "vUnCom":"1.00",
         "infADProd":"CONSULTA CARDIOLOGIA"
      },
      { 
         "cProd":1,
         "vProd":"1.00",
         "qCOM":"1",
         "vUnCom":"1.00",
         "infADProd":"ECG - ELETROCARDIOGRAMA"
      }
   ]
}        
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
          
            flash("etapa4")
            return render_template('emite_notafiscal.html', aloha='Sucesso')    
          
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
    