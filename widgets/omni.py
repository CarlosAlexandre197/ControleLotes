from PyQt6.QtWidgets import (
    QGroupBox,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QAbstractItemView,
    QHeaderView
)
from PyQt6.QtCore import Qt


class OmniWidget(QGroupBox):

    def __init__(self):
        super().__init__("OmniChannel")

        self.criar_componentes()
        self.criar_layout()
        self.configurar_tabela()

    # ==================================
    # CRIAÇÃO DOS COMPONENTES
    # ==================================

    def criar_componentes(self):

        self.quantidade = QLineEdit()
        self.quantidade.setObjectName("omni_quantidade")
        self.quantidade.setPlaceholderText(
            "Quantidade de pedidos"
        )

        self.botao_adicionar = QPushButton(
            "Adicionar"
        )
        self.botao_adicionar.setObjectName(
            "botao_add_omni"
        )

        self.lbl_total = QLabel(
            "Total OmniChannel: 0"
        )
        self.lbl_total.setObjectName(
            "lbl_total_omni"
        )

        self.tabela = QTableWidget()

        self.tabela.setObjectName(
            "tabela_omni"
        )

    # ==================================
    # CONFIGURAÇÃO DA TABELA
    # ==================================

    def configurar_tabela(self):

        self.tabela.setColumnCount(3)

        self.tabela.setHorizontalHeaderLabels([
            "ID",
            "Quantidade",
            "Hora"
        ])

        self.tabela.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.tabela.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.tabela.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.tabela.verticalHeader().setVisible(False)

        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.tabela.setAlternatingRowColors(True)

    # ==================================
    # LAYOUT
    # ==================================

    def criar_layout(self):

        entrada_layout = QHBoxLayout()

        entrada_layout.addWidget(
            self.quantidade
        )

        entrada_layout.addWidget(
            self.botao_adicionar
        )

        layout = QVBoxLayout()

        layout.addLayout(
            entrada_layout
        )

        layout.addWidget(
            self.tabela
        )

        layout.addWidget(
            self.lbl_total
        )

        self.setLayout(layout)

    # ==================================
    # ADICIONAR OMNICHANNEL
    # ==================================

    def adicionar(self):

        texto = self.quantidade.text().strip()

        if not texto:
            return

        try:
            quantidade = int(texto)

        except ValueError:
            return

        if quantidade <= 0:
            return

        linha = self.tabela.rowCount()

        self.tabela.insertRow(linha)

        id_lancamento = linha + 1

        hora = datetime.now().strftime("%H:%M")

        self.tabela.setItem(
            linha,
            0,
            QTableWidgetItem(
                str(id_lancamento)
            )
        )

        self.tabela.setItem(
            linha,
            1,
            QTableWidgetItem(
                str(quantidade)
            )
        )

        self.tabela.setItem(
            linha,
            2,
            QTableWidgetItem(
                hora
            )
        )

        self.quantidade.clear()

        self.atualizar_total()

    # ==================================
    # ATUALIZAR TOTAL
    # ==================================

    def atualizar_total(self):

        total = 0

        for linha in range(
            self.tabela.rowCount()
        ):

            item = self.tabela.item(
                linha,
                1
            )

            if item:

                total += int(
                    item.text()
                )

        self.lbl_total.setText(
            f"Total OmniChannel: {total}"
        )

    # ==================================
    # PEGAR TOTAL
    # ==================================

    def obter_total(self):

        total = 0

        for linha in range(
            self.tabela.rowCount()
        ):

            item = self.tabela.item(
                linha,
                1
            )

            if item:

                total += int(
                    item.text()
                )

        return total