from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QCheckBox,
    QTableWidget,
    QTableWidgetItem
)
from PySide6.QtCore import Qt
from datetime import datetime
from banco import (
    salvar_lote,
    buscar_lotes_do_dia,
    excluir_lote_db
)

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🚛 Controle de Lotes")
        self.resize(1200, 700)

        widget = QWidget()
        self.setCentralWidget(widget)

        layout_principal = QVBoxLayout(widget)

        titulo = QLabel("🚛 CONTROLE DE LOTES")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            padding:10px;
        """)

        layout_principal.addWidget(titulo)

        formulario = QFormLayout()

        self.lote = QLineEdit()
        self.quantidade = QLineEdit()
        self.cartoes = QLineEdit()
        self.cancelados = QLineEdit()
        self.palete = QLineEdit()
        self.montador = QLineEdit()
        self.caixas = QLineEdit()

        formulario.addRow("Lote:", self.lote)
        formulario.addRow("Quantidade:", self.quantidade)
        formulario.addRow("Cartões:", self.cartoes)
        formulario.addRow("Cancelados:", self.cancelados)
        formulario.addRow("Palete:", self.palete)
        formulario.addRow("Montador:", self.montador)
        formulario.addRow("Caixas do Palete:", self.caixas)

        layout_principal.addLayout(formulario)
        
        self.etiquetas = QCheckBox("Imprimiu Etiquetas")
        self.faturado = QCheckBox("Faturado")
        self.embarcou = QCheckBox("Embarcou")
        self.pre = QCheckBox("Pré-Autorização")
        self.notas = QCheckBox("Imprimiu Notas")

        layout_principal.addWidget(self.etiquetas)
        layout_principal.addWidget(self.faturado)
        layout_principal.addWidget(self.embarcou)
        layout_principal.addWidget(self.pre)
        layout_principal.addWidget(self.notas)

        botoes = QHBoxLayout()

        self.salvar = QPushButton("Salvar")
        self.limpar = QPushButton("Limpar")
        self.excluir = QPushButton("Excluir Lote")

        botoes.addWidget(self.salvar)
        botoes.addWidget(self.limpar)
        botoes.addWidget(self.excluir)
        
        self.salvar.clicked.connect(self.salvar_lote)
        self.limpar.clicked.connect(self.limpar_campos)
        self.excluir.clicked.connect(self.excluir_lote)

        layout_principal.addLayout(botoes)

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(9)
        self.tabela.setHorizontalHeaderLabels([
            "Lote",
            "Quantidade",
            "Cartões",
            "Cancelados",
            "Final",
            "Palete",
            "Montador",
            "Caixas",
            "Data"

        ])
        
        self.lbl_total_lotes = QLabel("Total de Lotes: 0")
        self.lbl_total_pedidos = QLabel("Total Final de Pedidos: 0")
        self.lbl_total_caixas = QLabel("Total de Caixas: 0")
        layout_principal.addWidget(self.tabela)
        layout_principal.addWidget(self.lbl_total_lotes)
        layout_principal.addWidget(self.lbl_total_pedidos)
        layout_principal.addWidget(self.lbl_total_caixas)
        self.carregar_lotes_do_dia()
        
    def salvar_lote(self):

            lote = self.lote.text()
            quantidade = int(self.quantidade.text() or 0)
            cartoes = int(self.cartoes.text() or 0)
            cancelados = int(self.cancelados.text() or 0)

            palete = self.palete.text()
            montador = self.montador.text()
            caixas = int(self.caixas.text() or 0)

            final = quantidade - cartoes - cancelados
            data = datetime.now().strftime("%d/%m/%Y")

            linha = self.tabela.rowCount()
            self.tabela.insertRow(linha)

            self.tabela.setItem(linha, 0, QTableWidgetItem(lote))
            self.tabela.setItem(linha, 1, QTableWidgetItem(str(quantidade)))
            self.tabela.setItem(linha, 2, QTableWidgetItem(str(cartoes)))
            self.tabela.setItem(linha, 3, QTableWidgetItem(str(cancelados)))
            self.tabela.setItem(linha, 4, QTableWidgetItem(str(final)))
            self.tabela.setItem(linha, 5, QTableWidgetItem(palete))
            self.tabela.setItem(linha, 6, QTableWidgetItem(montador))
            self.tabela.setItem(linha, 7, QTableWidgetItem(str(caixas)))
            self.tabela.setItem(linha, 8, QTableWidgetItem(data))

            self.atualizar_totais()
            
            # Limpar campos
            self.lote.clear()
            self.quantidade.clear()
            self.cartoes.clear()
            self.cancelados.clear()
            self.palete.clear()
            self.montador.clear()
            self.caixas.clear()

            # Desmarcar checkboxes
            self.etiquetas.setChecked(False)
            self.faturado.setChecked(False)
            self.embarcou.setChecked(False)
            self.pre.setChecked(False)
            self.notas.setChecked(False)
            
            print("SALVANDO NO SQLITE")
            
            salvar_lote(
                lote,
                quantidade,
                cartoes,
                cancelados,
                final,
                palete,
                montador,
                caixas,
                data
            )
            
            self.limpar_campos()

    def limpar_campos(self):

        self.lote.clear()
        self.quantidade.clear()
        self.cartoes.clear()
        self.cancelados.clear()
        self.palete.clear()
        self.montador.clear()
        self.caixas.clear()
        
    def carregar_lotes_do_dia(self):
        
        data = datetime.now().strftime("%d/%m/%Y")

        lotes = buscar_lotes_do_dia(data)

        for lote in lotes:
            linha = self.tabela.rowCount()
            self.tabela.insertRow(linha)

            for coluna, valor in enumerate(lote):
                self.tabela.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(str(valor))
                )

        self.atualizar_totais()

    def atualizar_totais(self):

        total_lotes = self.tabela.rowCount()

        total_pedidos = 0
        total_caixas = 0

        for linha in range(total_lotes):

            final = int(self.tabela.item(linha, 4).text())
            caixas = int(self.tabela.item(linha, 7).text())

            total_pedidos += final
            total_caixas += caixas

        self.lbl_total_lotes.setText(
            f"Total de Lotes: {total_lotes}"
        )

        self.lbl_total_pedidos.setText(
            f"Total Final de Pedidos: {total_pedidos}"
        )

        self.lbl_total_caixas.setText(
            f"Total de Caixas: {total_caixas}"
        )   
        
    def excluir_lote(self):

        linha = self.tabela.currentRow()

        if linha < 0:
            return

        lote = self.tabela.item(linha, 0).text()

        excluir_lote_db(lote)

        self.tabela.removeRow(linha)

        self.atualizar_totais()