from PyQt6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QTableWidgetItem
)

from PyQt6.uic import loadUi
from datetime import datetime

from banco import salvar_lote, buscar_lotes_do_dia


class Interface(QMainWindow):

    def __init__(self):
        super().__init__()

        loadUi("interface.ui", self)

        self.configurar_tabela()

        self.botao_salvar.clicked.connect(self.salvar)

        self.carregar_lotes_do_dia()
        self.atualizar_totais()


    # ==============================
    # CONFIGURAÇÃO DA TABELA
    # ==============================

    def configurar_tabela(self):

        self.tabela.setColumnCount(8)

        self.tabela.setHorizontalHeaderLabels([
            "Lote",
            "Quantidade",
            "Cartões",
            "Cancelados",
            "Quantidade Final",
            "Palete",
            "Montador",
            "Caixas"
        ])


    # ==============================
    # SALVAR LOTE
    # ==============================

    def salvar(self):

        lote = self.lote.text()
        quantidade = int(self.quantidade.text())
        cartoes = int(self.cartoes.text())
        cancelados = int(self.cancelados.text())

        palete = self.palete.text()
        montador = self.montador.text()
        caixas = int(self.caixas.text())


        quantidade_final = (
            quantidade
            - cartoes
            - cancelados
        )


        if quantidade_final < 0:
            QMessageBox.warning(
                self,
                "Erro",
                "Quantidade final não pode ser negativa."
            )
            return


        data = datetime.now().strftime("%d/%m/%Y")


        salvar_lote(
            lote,
            quantidade,
            cartoes,
            cancelados,
            quantidade_final,
            palete,
            montador,
            caixas,
            data
        )


        self.carregar_lotes_do_dia()

        self.atualizar_totais()

        self.limpar_campos()



    # ==============================
    # CARREGAR LOTES
    # ==============================

    def carregar_lotes_do_dia(self):

        data = datetime.now().strftime("%d/%m/%Y")


        lotes = buscar_lotes_do_dia(data)


        self.tabela.setRowCount(0)


        for lote in lotes:

            linha = self.tabela.rowCount()

            self.tabela.insertRow(linha)


            for coluna, valor in enumerate(lote):

                self.tabela.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(str(valor))
                )



    # ==============================
    # ATUALIZAR TOTAIS
    # ==============================

    def atualizar_totais(self):

        total_pedidos = 0
        total_caixas = 0


        for linha in range(self.tabela.rowCount()):

            total_pedidos += int(
                self.tabela.item(
                    linha,
                    4
                ).text()
            )


            total_caixas += int(
                self.tabela.item(
                    linha,
                    7
                ).text()
            )


        self.total_pedidos.setText(
            str(total_pedidos)
        )

        self.total_caixas.setText(
            str(total_caixas)
        )



    # ==============================
    # LIMPAR CAMPOS
    # ==============================

    def limpar_campos(self):

        self.lote.clear()
        self.quantidade.clear()
        self.cartoes.clear()
        self.cancelados.clear()
        self.palete.clear()
        self.montador.clear()
        self.caixas.clear()
    
if __name__ == "__main__":

    from PyQt6.QtWidgets import QApplication

    app = QApplication([])

    janela = Interface()

    janela.show()

    app.exec()    
