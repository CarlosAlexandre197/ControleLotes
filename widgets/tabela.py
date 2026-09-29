from PyQt6.QtWidgets import (
    QTableWidget,
    QAbstractItemView,
    QHeaderView
)


class TabelaWidget(QTableWidget):

    def __init__(self):
        super().__init__()

        self.configurar_tabela()

    def configurar_tabela(self):

        self.setColumnCount(10)

        self.setHorizontalHeaderLabels([
            "Nº",
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

        self.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.verticalHeader().setVisible(False)

        self.setAlternatingRowColors(True)

        self.setSizeAdjustPolicy(
            QTableWidget.SizeAdjustPolicy.AdjustToContents
        )

        self.setStyleSheet("""
            QTableWidget {
                selection-background-color: #cfe8ff;
                selection-color: #1f1f1f;
            }
        """)