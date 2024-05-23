
def test_vazio():
    print


def limpar_campos(tela):

    tela.produtoTipo.clear()
    tela.produtoMarca.clear()
    tela.produtoModelo.clear()
    tela.produtoValor.clear()
    tela.radioPeriferico.setChecked(False)
    tela.radioHardware.setChecked(False)
    tela.radioEletronico.setChecked(False)
    
    

