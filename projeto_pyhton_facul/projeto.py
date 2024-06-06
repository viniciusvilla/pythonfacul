import funcoes
from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QMessageBox
import mysql.connector
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

info_produtos = {}
numero_id = 0
#conexão com banco de dados
banco = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "facul123",
    database = "projeto_facul"

)

def cadastrar():
    """
    Função responsável pelo armazenamento dos valores em relação aos produtos em suas respectivas variavéis dentro do dicionário "info_produtos" e também ao envio (cadastro) das mesmas ao banco de dados.

    """
    
    #Parte responsável pelos radios de categoria da tela_cadastro.
    
    if(tela_cadastro.radioPeriferico.isChecked()):
        info_produtos['categoria'] = 'Periférico'
        
    elif(tela_cadastro.radioHardware.isChecked()):
        info_produtos['categoria'] = 'Hardware'
        
    elif(tela_cadastro.radioEletronico.isChecked()):
        info_produtos['categoria'] = 'Eletrônico'

    else:
        #Se nenhum dos radios anteriores foram selecionados, será acionada essa tela de alerta e o método return, impedindo do usúario proceder com o cadastro.

        QMessageBox.about(tela_cadastro, '[ALERTA]', 'CATEGORIA não escolhida')
        return

    #Parte responsável pelo armazenamento dos valores dos inputs (caixas de texto) da tela_cadastro no dicionário info_produtosææ.

    info_produtos['tipo'] = tela_cadastro.produtoTipo.text()
        
    info_produtos['marca'] = tela_cadastro.produtoMarca.text()
        
    info_produtos['modelo'] = tela_cadastro.produtoModelo.text()

    #Se algum dos inputs (caixas de texto) anteriores não foram preenchidos, isso é, estiver em branco, será chamada a mensagem de alerta e o metodo "return" impedindo do usúario proceder com o cadastro.

    if not (info_produtos['tipo']):
        QMessageBox.about(tela_cadastro, '[ALERTA]', 'TIPO não preenchido')
        return
    
    elif not (info_produtos['marca']):
         QMessageBox.about(tela_cadastro, '[ALERTA]', 'MARCA não preenchida')
         return
    
    elif not (info_produtos['modelo']):
         QMessageBox.about(tela_cadastro, '[ALERTA]', 'MODELO não preenchido')
         return

    #Parte responsável pela verificação de valor de texto no input de "valor" na tela_cadastro, só sera aceito valores numerais, caso contrário, será exibida a mensagem de alerta e acionado o metodo return, impedindo o usúario de proceder com o código.

    while True:
        try:
            info_produtos['valor'] = float(tela_cadastro.produtoValor.text())
            
        except(ValueError, TypeError):
             QMessageBox.about(tela_cadastro, '[ALERTA]', 'Valor inválido')
             return
        break
        
                
    #Parte responsável pelo envio dos dados da tela_cadastro ao banco de dados MySQL.
    try:
        cursor = banco.cursor()
        comando_SQL = "INSERT INTO produtos (categoria, tipo, marca, modelo, valor) VALUES (%s, %s, %s, %s, %s)"
        dados = (str(info_produtos['categoria']), str(info_produtos['tipo']), str(info_produtos['marca']), str(info_produtos['modelo']), str(info_produtos['valor']))
        cursor.execute(comando_SQL, dados)
        banco.commit()

        QMessageBox.about(tela_cadastro, '[SUCESSO]', 'Produto cadastrado com sucesso!')

        info_produtos.clear()
        funcoes.limpar_campos(tela_cadastro)

        if (tela_banco.isVisible() == True):
            banco_de_dados()
        
        
    except mysql.connector.Error as err:
        QMessageBox.about(tela_cadastro, '[ALERTA]', f'Erro ao conectar ao banco de dados: {err}')


def banco_de_dados():
    """
    Função responsável pela exibição da tela_banco, e também da exibição da tabela do banco de dados MySQL.

    dados_lidos: salva o comando select*from produtos, ou seja, salva os dados cadastrados no banco de dados MySQL.'

    Contador (for): Exibição da tabela em linhas (l) e colunas (c) inserindo os valores no elemento tableWidget da tela_banco. 
    
    Como as quantidades de linhas são mutaveis, o parâmetro utilizado foi len(dados_lidos), a coluna é fixa (6 elementos) então o parâmetro foi até 6.

    """
    tela_banco.show()

    cursor = banco.cursor()
    comando_SQL = "select * from produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    tela_banco.tableWidget.setRowCount(len(dados_lidos))
    tela_banco.tableWidget.setColumnCount(6)
    
    for l in range (0, len(dados_lidos)):
        for c in range (6):
            tela_banco.tableWidget.setItem(l, c, QtWidgets.QTableWidgetItem(str(dados_lidos[l][c])))


def editar_dados():
    """
    Função responsável pela exibição da tela_editar e também pela inserção dos dados desejados para edição em seus respectivos campos.

    linha_selecionada: Variável que armazena a linha selecionada (clicada) pelo usúario pelo metódo de currentRow().

    dados_lidos: Variável que recebe os id que estão armazenados no banco de dados MySQL.

    valor_id: Variável que recebe o valor de dados_lidos no primeiro indice da linha_selecionada pelo usúario, ou seja, o id da linha selecionada pelo usúario.

    numero_id: Variável global criada para armazenar o valor_id e poder trabalhar junto da função salvar_dados_editados.

    """
    global numero_id

    tela_editar.show()

    linha_selecionada = tela_banco.tableWidget.currentRow()
    
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha_selecionada][0]
    numero_id = valor_id
    

    cursor.execute("SELECT * FROM produtos WHERE id="+str(valor_id))
    produto = cursor.fetchall()
    
    #Parte responsável por pegar os dados do banco de dados e colocar em suas respectivas caixas de texto.
    tela_editar.editor_tipo.setText(str(produto[0][2]))
    tela_editar.editor_marca.setText(str(produto[0][3]))
    tela_editar.editor_modelo.setText(str(produto[0][4]))
    tela_editar.editor_valor.setText(str(produto[0][5]))


def salvar_dados_editados():
    """
    Função responsalvel por salvar os dados inserido na tela_editar por meio da função editar_dados. Ou seja, essa função trabalha em conjunto com a anterior (editar_dados)

    numero_id: variavél que armazena o valor_id especificado na função editar_dados

    categoria, tipo, marca, modelo: Variáveis responsáveis pelo armazenamento de valores respectivos as suas caixas de texto da tela_editar.
    
    
    """
    global numero_id

    #Parte responsável pelos radios de categoria da tela_editar.
    if(tela_editar.radioED_periferico.isChecked()):
        categoria = 'Periférico'
        
    elif(tela_editar.radioED_hardware.isChecked()):
        categoria = 'Hardware'

    elif(tela_editar.radioED_eletronico.isChecked()):
        categoria = 'Eletrônico'

    else:
        #Se nenhum dos radios anteriores foram selecionados, será acionada essa tela de alerta e o método return, impedindo do usúario proceder com a edição.
        QMessageBox.about(tela_editar, '[ALERTA]', 'CATEGORIA não escolhida')
        return
    
    tipo = tela_editar.editor_tipo.text()
    marca = tela_editar.editor_marca.text()
    modelo = tela_editar.editor_modelo.text()

    #Se algum dos inputs (caixas de texto) anteriores não foram preenchidos, isso é, estiver em branco, será chamada a mensagem de alerta e o metodo "return" impedindo do usúario proceder com a edição.
    
    if not (tipo):
        QMessageBox.about(tela_editar, '[ALERTA]', 'TIPO não preenchido')
        return
    elif not (marca):
        QMessageBox.about(tela_editar, '[ALERTA]', 'MARCA não preenchido')
        return
    elif not (modelo):
        QMessageBox.about(tela_editar, '[ALERTA]', 'MODELO não preenchido')
        return
    
    while True:
        try:
            valor = float(tela_editar.editor_valor.text())
            
            
        except(ValueError, TypeError):
             QMessageBox.about(tela_editar, '[ALERTA]', 'Valor inválido')
             return
        break

    try:
        #Parte do código que inseri os valores editados no banco de dados MySQL, onde a referencia será o número_id.

        QMessageBox.about(tela_editar, '[SUCESSO]', 'Dados Atualizados')
        cursor = banco.cursor()
        comando_sql = "UPDATE produtos SET categoria = %s, tipo = %s, marca = %s, modelo = %s, valor = %s WHERE id = %s"
        valores = (categoria, tipo, marca, modelo, valor, numero_id)
        cursor.execute(comando_sql, valores)
        banco.commit()

        tela_editar.close()
        tela_banco.close()
        banco_de_dados()
        

    except mysql.connector.Error as err:
        QMessageBox.about(tela_editar, '[ALERTA]', f'Erro ao conectar ao banco de dados: {err}')

#Procedimento para carregar as telas do programa.
app = QtWidgets.QApplication([])
tela_cadastro=uic.loadUi('telas/tela_cadastro.ui')
tela_banco=uic.loadUi('telas/tela_banco.ui')
tela_editar=uic.loadUi('telas/tela_editar.ui')

#Ligando os eventos de click dos botões as suas respectivas funções.
tela_cadastro.btnCadastrar.clicked.connect(cadastrar)
tela_cadastro.btnBanco.clicked.connect(banco_de_dados)
tela_banco.btnPDF.clicked.connect(lambda: funcoes.gerar_pdf(banco, tela_banco))
tela_banco.btnExcluir.clicked.connect(lambda: funcoes.excluir_dados(tela_banco, banco))
tela_banco.btnEditar.clicked.connect(editar_dados)
tela_editar.btnSalvar.clicked.connect(salvar_dados_editados)

#Carregando a tela de cadastro.
tela_cadastro.show()
app.exec()