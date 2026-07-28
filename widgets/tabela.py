from PyQt6.QtWidgets import (
    QTableWidget,
    QAbstractItemView,
    QHeaderView
)


class TabelaWidget(QTableWidget):

    def __init__(self):
        super().__init__()

        self.configurar_tabela()

    # ==================================
    # CONFIGURAÇÃO DA TABELA
    # ==================================

    def configurar_tabela(self):

        self.setColumnCount(9)

        self.setHorizontalHeaderLabels([
            "Lote",
            "Quantidade",
            "Cartões",
            "Cancelados",
            "Quantidade Final",
            "Palete",
            "Montador",
            "Caixas",
            "Status"
        ])

        # Seleciona a linha inteira
        self.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        # Permite selecionar apenas uma linha
        self.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        # Não permite editar diretamente na tabela
        self.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        # Ajusta automaticamente a largura das colunas
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        # Esconde a numeração das linhas
        self.verticalHeader().setVisible(False)

        # Alterna a cor das linhas para facilitar a leitura
        self.setAlternatingRowColors(True)

        # A tabela ocupa todo o espaço disponível
        self.setSizeAdjustPolicy(
            QTableWidget.SizeAdjustPolicy.AdjustToContents
        )