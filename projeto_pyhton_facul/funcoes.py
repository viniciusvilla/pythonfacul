from PyQt5.QtWidgets import QMessageBox
import mysql.connector
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyQt5.QtWidgets import QFileDialog


def excluir_dados(tela_banco, banco):
    """
    Função responsável pela exclusão de linhas, tanto da tabela exibida no programa, quanto da tabela do banco de dados MySQL.

    linha_selecionada: Variável que armazena a linha selecionada (clicada) pelo usúario pelo metódo de currentRow().

    dados_lidos: Variável que recebe os id que estão armazenados no banco de dados MySQL.

    valor_id: Variável que recebe o valor de dados_lidos no primeiro indice da linha_selecionada pelo usúario, ou seja, o id da linha selecionada pelo usúario.

    """
    #Parte responsável pela tela de mensagem de confimação de exclusão pelo usúario.

    msg = QMessageBox(tela_banco)
    msg.setStyleSheet("background-color: rgb(255, 255, 255);")
    msg.setWindowTitle('Confirmar Exclusão')
    msg.setText('Tem certeza que deseja EXCLUIR a linha selecionada?')
    msg.setIcon(QMessageBox.Question)
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    button_yes = msg.button(QMessageBox.Yes)
    button_yes.setText('Sim')
    button_no = msg.button(QMessageBox.No)
    button_no.setText('Não')

    resposta = msg.exec_()

    #Caso a resposta seja "NÃO", é acionado o metodo return, impedindo a exclusão da linha selecionada.
    if resposta == QMessageBox.No:
        return

    #Remove da tableWidget a linha selecionada para remoção.
    linha_selecionada = tela_banco.tableWidget.currentRow()
    tela_banco.tableWidget.removeRow(linha_selecionada)

    
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha_selecionada][0]

    #Por fim, exlclui a linha no banco de dados MySQL seguindo como parâmetro o id do valor_id.
    cursor.execute("DELETE FROM produtos WHERE id=" + str(valor_id))
    banco.commit()


def gerar_pdf(banco, tela_banco):
    try:
        pdf_cursor = banco.cursor()
        comando_SQL = "SELECT * FROM produtos"
        pdf_cursor.execute(comando_SQL)
        dados_lidos = pdf_cursor.fetchall()

        # Abrir diálogo para seleção de arquivo
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(tela_banco, "Salvar PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if fileName:
        
            # Configuração inicial do PDF
            pdf = canvas.Canvas(fileName, pagesize=A4)
            largura, altura = A4
            pdf.setFont("Times-Bold", 25)
            pdf.drawString(185, 800, "Produtos cadastrados")
            
            # Definição do cabeçalho da tabela
            pdf.setFont("Times-Bold", 18)
            pdf.drawString(20, 750, "CATEGORIA")
            pdf.drawString(160, 750, "TIPO")
            pdf.drawString(310, 750, "MARCA")
            pdf.drawString(410, 750, "MODELO")
            pdf.drawString(510, 750, "VALOR")
            
            pdf.setFont("Times-Roman", 12)
            y = 0
            
            # Adicionar os dados ao PDF
            for i in range(len(dados_lidos)):
                y += 20
                if 750 - y < 50:  # Verificar se é necessário adicionar uma nova página
                    pdf.showPage()
                    pdf.setFont("Times-Bold", 18)
                    pdf.drawString(20, 800, "CATEGORIA")
                    pdf.drawString(160, 800, "TIPO")
                    pdf.drawString(310, 800, "MARCA")
                    pdf.drawString(410, 800, "MODELO")
                    pdf.drawString(510, 800, "VALOR")
                    pdf.setFont("Times-Roman", 12)
                    y = 0
                
                pdf.drawString(20, 750 - y, str(dados_lidos[i][1]))
                pdf.drawString(160, 750 - y, str(dados_lidos[i][2]))
                pdf.drawString(310, 750 - y, str(dados_lidos[i][3]))
                pdf.drawString(410, 750 - y, str(dados_lidos[i][4]))
                pdf.drawString(510, 750 - y, f"{dados_lidos[i][5]:.2f}")  # Formatando o valor para duas casas decimais
            
            pdf.save()
            QMessageBox.about(tela_banco, '[SUCESSO]', 'PDF gerado com sucesso!')
            
    except mysql.connector.Error as err:
        print(f'Erro ao conectar ao banco de dados: {err}')
        QMessageBox.about(tela_banco, '[ERRO]', f'Erro ao gerar PDF: {err}')


def limpar_campos(tela_cadastro):
    """
    Função responsavel pela limpeza dos campos (inputs) da tela_cadastro toda vez que o usúario clicar no botão "cadastrar" (btnCadastrar)

    """

    tela_cadastro.produtoTipo.clear()
    tela_cadastro.produtoMarca.clear()
    tela_cadastro.produtoModelo.clear()
    tela_cadastro.produtoValor.clear()
    tela_cadastro.radioPeriferico.setAutoExclusive(False)
    tela_cadastro.radioHardware.setAutoExclusive(False)
    tela_cadastro.radioEletronico.setAutoExclusive(False)
    tela_cadastro.radioPeriferico.setChecked(False)
    tela_cadastro.radioHardware.setChecked(False)
    tela_cadastro.radioEletronico.setChecked(False)
    tela_cadastro.radioPeriferico.setAutoExclusive(True)
    tela_cadastro.radioHardware.setAutoExclusive(True)
    tela_cadastro.radioEletronico.setAutoExclusive(True)
    
    

