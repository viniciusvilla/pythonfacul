import funcoes
from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QMessageBox
import mysql.connector
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

numero_id = 0

banco = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "facul123",
    database = "projeto_facul"

)


info_produtos = {}
produtos = []

def cadastrar():
    print('funcao')
    
    if(tela_cadastro.radioPeriferico.isChecked()):
        info_produtos['categoria'] = 'Periférico'
        
    elif(tela_cadastro.radioHardware.isChecked()):
        info_produtos['categoria'] = 'Hardware'
        
    elif(tela_cadastro.radioEletronico.isChecked()):
        info_produtos['categoria'] = 'Eletrônico'

    else:
        QMessageBox.about(tela_cadastro, '[ALERTA]', 'CATEGORIA não escolhida')
        return

    
    info_produtos['tipo'] = tela_cadastro.produtoTipo.text()
        
    info_produtos['marca'] = tela_cadastro.produtoMarca.text()
        
    info_produtos['modelo'] = tela_cadastro.produtoModelo.text()

    if not (info_produtos['tipo']):
        QMessageBox.about(tela_cadastro, '[ALERTA]', 'TIPO não preenchido')
        return
    
    elif not (info_produtos['marca']):
         QMessageBox.about(tela_cadastro, '[ALERTA]', 'MARCA não preenchida')
         return
    
    elif not (info_produtos['modelo']):
         QMessageBox.about(tela_cadastro, '[ALERTA]', 'MODELO não preenchido')
         return


    while True:
        try:
            info_produtos['valor'] = float(tela_cadastro.produtoValor.text())
            
        except(ValueError, TypeError):
             QMessageBox.about(tela_cadastro, '[ALERTA]', 'Valor inválido')
             return
        break
        
        
    produtos.append(info_produtos.copy())
    
        
    print()
    for i in produtos:
        for k,v in i.items():
            print(f'{k}: {v}')
        print()

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
    global numero_id

    print('editar')
    tela_editar.show()

    linha_selecionada = tela_banco.tableWidget.currentRow()
    

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha_selecionada][0]
    numero_id = valor_id
    

    cursor.execute("SELECT * FROM produtos WHERE id="+str(valor_id))
    produto = cursor.fetchall()
    print(produto)
    
    
    tela_editar.editor_tipo.setText(str(produto[0][2]))
    tela_editar.editor_marca.setText(str(produto[0][3]))
    tela_editar.editor_modelo.setText(str(produto[0][4]))
    tela_editar.editor_valor.setText(str(produto[0][5]))


def salvar_dados():
    global numero_id
    print(numero_id)

    if(tela_editar.radioED_periferico.isChecked()):
        categoria = 'Periférico'
        
    elif(tela_editar.radioED_hardware.isChecked()):
        categoria = 'Hardware'

    elif(tela_editar.radioED_eletronico.isChecked()):
        categoria = 'Eletrônico'

    else:
        QMessageBox.about(tela_editar, '[ALERTA]', 'CATEGORIA não escolhida')
        return
    
    tipo = tela_editar.editor_tipo.text()
    marca = tela_editar.editor_marca.text()
    modelo = tela_editar.editor_modelo.text()
    
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


app = QtWidgets.QApplication([])
tela_cadastro=uic.loadUi('telas/tela_cadastro.ui')
tela_banco=uic.loadUi('telas/tela_banco.ui')
tela_editar=uic.loadUi('telas/tela_editar.ui')

tela_cadastro.btnCadastrar.clicked.connect(cadastrar)
tela_cadastro.btnBanco.clicked.connect(banco_de_dados)
tela_banco.btnPDF.clicked.connect(lambda: funcoes.gerar_pdf(tela_cadastro, banco, tela_banco))
tela_banco.btnExcluir.clicked.connect(lambda: funcoes.excluir_dados(tela_banco, banco))
tela_banco.btnEditar.clicked.connect(editar_dados)
tela_editar.btnSalvar.clicked.connect(salvar_dados)

tela_cadastro.show()
app.exec()