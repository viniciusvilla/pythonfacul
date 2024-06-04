from PyQt5.QtWidgets import QMessageBox
import mysql.connector
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyQt5.QtWidgets import QFileDialog


def excluir_dados(tela_banco, banco):

    msg = QMessageBox(tela_banco)
    msg.setStyleSheet("background-color: #f1f1f1;")
    msg.setWindowTitle('Confirmar Exclusão')
    msg.setText('Tem certeza que deseja EXCLUIR a linha selecionada?')
    msg.setIcon(QMessageBox.Question)
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    button_yes = msg.button(QMessageBox.Yes)
    button_yes.setText('Sim')
    button_no = msg.button(QMessageBox.No)
    button_no.setText('Não')

    resposta = msg.exec_()

    if resposta == QMessageBox.No:
        return

    linha_selecionada = tela_banco.tableWidget.currentRow()
    tela_banco.tableWidget.removeRow(linha_selecionada)
    print(f'Linha selecionada {linha_selecionada}')

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    print(f'Dados lidos: {dados_lidos}')
    valor_id = dados_lidos[linha_selecionada][0]
    print(f'Dados lidos no indice linha selecionada: {valor_id}')

    cursor.execute("DELETE FROM produtos WHERE id=" + str(valor_id))
    banco.commit()


def gerar_pdf(tela_cadastro, banco, tela_banco):
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
            print('PDF GERADO')
            QMessageBox.about(tela_cadastro, '[SUCESSO]', 'PDF gerado com sucesso!')
            
    except mysql.connector.Error as err:
        print(f'Erro ao conectar ao banco de dados: {err}')
        QMessageBox.about(tela_cadastro, '[ERRO]', f'Erro ao gerar PDF: {err}')


def limpar_campos(tela_cadastro):

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
    
    

