import funcoes
from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QMessageBox


info_produtos = {}
produtos = []

def cadastrar():
    print('funcao')
    
    if(tela.radioPeriferico.isChecked()):
        info_produtos['categoria'] = 'Periférico'
        
    if(tela.radioHardware.isChecked()):
        info_produtos['categoria'] = 'Hardware'
        
    if(tela.radioEletronico.isChecked()):
        info_produtos['categoria'] = 'Eletrônico'
        
    
    info_produtos['tipo'] = tela.produtoTipo.text()
    
    info_produtos['marca'] = tela.produtoMarca.text()
     
    info_produtos['modelo'] = tela.produtoModelo.text()
    
    while True:
        try:
            info_produtos['valor'] = float(tela.produtoValor.text())
            tela.lblErro.setText('')
            
        except(ValueError, TypeError):
            tela.lblErro.setText('[ERRO] Valor inválido. Por favor digite um número.')
            return
        break
        
        
    produtos.append(info_produtos.copy())
    info_produtos.clear()
    funcoes.limpar_campos(tela)
        
    print()
    for i in produtos:
        for k,v in i.items():
            print(f'{k}: {v}')
        print()
              
  
app = QtWidgets.QApplication([])
tela=uic.loadUi('tela_cadastro.ui')

tela.btnCadastrar.clicked.connect(cadastrar)

tela.show()
app.exec()